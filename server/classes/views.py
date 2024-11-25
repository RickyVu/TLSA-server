from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Class
from .serializers import ClassSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from tlsa_server.permissions import IsTeacher, IsStudent

# Create your views here.
class ClassView(APIView):
    serializer_class = ClassSerializer

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
                    "message": "Class created successfully.",
                    "class": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='class_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Class ID to retrieve',
                required=True,
            ),
        ],
        responses={
            200: ClassSerializer,
            400: {'error': 'class_id parameter is required'},
            404: {'error': 'Class not found'},
        },
    )
    def get(self, request, format=None):
        class_id = request.query_params.get('lab_id')
        if not class_id:
            return Response({"error": "class_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            class1 = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(class1)
        return Response(serializer.data)
