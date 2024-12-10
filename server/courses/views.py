from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, CourseEnrollmentSerializer, CourseClassSerializer
from tlsa_server.permissions import IsAuthenticated, IsTeacher

class CourseView(APIView):
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsTeacher()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
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
                required=False,
            ),
            OpenApiParameter(
                name='course_name',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Course name to retrieve (similarity)',
                required=False,
            ),
            OpenApiParameter(
                name='personal',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Get personal courses',
                required=False,
            ),
        ],
        responses={
            200: CourseSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        course_id = request.query_params.get('course_id')
        course_name = request.query_params.get('course_name')
        personal = request.query_params.get('personal')
        user = request.user

        filters = {}
        if course_id:
            filters["id"] = course_id
        if course_name:
            filters["name__icontains"] = course_name

        if personal and personal.lower()=="true":
            # Get courses that the user is enrolled in
            enrolled_courses = CourseEnrollment.objects.filter(student=user).values_list('course_id', flat=True)
            filters["id__in"] = enrolled_courses

        courses = Course.objects.filter(**filters)
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)

class CourseEnrollmentView(APIView):
    serializer_class = CourseEnrollmentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            enrollments = serializer.save()
            return Response(
                {
                    "message": "Students enrolled successfully.",
                    "enrollment": {
                        "student_ids": [enrollment.student.id for enrollment in enrollments],
                        "course_id": enrollments[0].course.id
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseClassView(APIView):
    serializer_class = CourseClassSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        return []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course_class = serializer.save()
            return Response(
                {
                    "message": "Class added to course successfully.",
                    "course_class": {
                        "class_id": course_class.class_instance.id,
                        "course_id": course_class.course.id
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)