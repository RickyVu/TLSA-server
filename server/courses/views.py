from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Course
from .serializers import CourseSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from tlsa_server.permissions import IsTeacher, IsStudent

# Create your views here.
class CourseView(APIView):
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsStudent()]
        elif self.request.method == 'POST':
            return [IsTeacher()]
        return []
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Course created successfully.",
                    "course": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='course_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Course ID to retrieve',
                required=True,
            ),
        ],
        responses={
            200: CourseSerializer,
            400: {'error': 'course_id parameter is required'},
            404: {'error': 'Course not found'},
        },
    )
    def get(self, request, format=None):
        course_id = request.query_params.get('lab_id')
        if not course_id:
            return Response({"error": "course_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(course)
        return Response(serializer.data)