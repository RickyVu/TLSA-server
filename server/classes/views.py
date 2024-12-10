from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter
from tlsa_server.permissions import IsAuthenticated, IsTeacher
from .models import (Class, 
                     TeachClass, 
                     ClassLocation, 
                     ClassComment)
from .serializers import (ClassSerializer, 
                          TeachClassSerializer, 
                          ClassLocationSerializer,
                          ClassCommentSerializer, ClassCommentWithoutSenderSerializer)
from courses.models import (CourseClass, CourseEnrollment)

class ClassView(APIView):
    serializer_class = ClassSerializer
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
            class_instance = serializer.save()
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
                required=False,
            ),
            OpenApiParameter(
                name='class_name',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Class name to retrieve (similarity)',
                required=False,
            ),
            OpenApiParameter(
                name='course_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Course ID to retrieve classes for',
                required=False,
            ),
            OpenApiParameter(
                name='personal',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Get personal classes',
                required=False,
            ),
        ],
        responses={
            200: ClassSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        class_id = request.query_params.get('class_id')
        class_name = request.query_params.get('class_name')
        course_id = request.query_params.get('course_id')
        personal = request.query_params.get('personal')
        user = request.user

        filters = {}
        if class_id:
            filters["id"] = class_id
        if class_name:
            filters["name__icontains"] = class_name

        if course_id:
            course_classes = CourseClass.objects.filter(course_id=course_id).values_list('class_instance_id', flat=True)
            filters["id__in"] = course_classes

        if personal and personal.lower()=="true":
            # Get courses that the user is enrolled in
            enrolled_courses = CourseEnrollment.objects.filter(student=user).values_list('course_id', flat=True)
            # Get classes that belong to the enrolled courses
            enrolled_classes = CourseClass.objects.filter(course_id__in=enrolled_courses).values_list('class_instance_id', flat=True)
            filters["id__in"] = enrolled_classes

        classes = Class.objects.filter(**filters)
        serializer = self.serializer_class(classes, many=True)
        return Response(serializer.data)


class TeacherClassView(APIView):
    serializer_class = TeachClassSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Teacher assigned to class successfully.",
                    "assignment": serializer.data
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
                description='Class ID to retrieve teachers',
                required=False,
            ),
            OpenApiParameter(
                name='class_name',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Class name to retrieve teachers (similarity)',
                required=False,
            ),
        ],
        responses={
            200: TeachClassSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        class_id = request.query_params.get('class_id')
        class_name = request.query_params.get('class_name')

        filters = {}
        if class_id:
            filters["class_id"] = class_id
        if class_name:
            classes = Class.objects.filter(name__icontains=class_name)
            filters["class_id__in"] = classes

        teachers = TeachClass.objects.filter(**filters)
        serializer = self.serializer_class(teachers, many=True)
        return Response(serializer.data)
    

class ClassLocationView(APIView):
    serializer_class = ClassLocationSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Location assigned to class successfully.",
                    "location": serializer.data
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
                description='Class ID to retrieve locations',
                required=False,
            ),
            OpenApiParameter(
                name='class_name',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Class name to retrieve locations (similarity)',
                required=False,
            ),
        ],
        responses={
            200: ClassLocationSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        class_id = request.query_params.get('class_id')
        class_name = request.query_params.get('class_name')

        filters = {}
        if class_id:
            filters["class_id"] = class_id
        if class_name:
            classes = Class.objects.filter(name__icontains=class_name)
            filters["class_id__in"] = classes

        locations = ClassLocation.objects.filter(**filters)
        serializer = self.serializer_class(locations, many=True)
        return Response(serializer.data)

class CommentToClassView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer_class = ClassCommentWithoutSenderSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            # Set the sender_id to the authenticated user's ID
            serializer.validated_data['sender_id'] = request.user
            serializer.save()
            return Response(
                {
                    "message": "Comment added successfully.",
                    "comment": serializer.data
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
                description='Class ID to retrieve comments',
                required=False,
            ),
            OpenApiParameter(
                name='sender_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Sender ID to retrieve comments',
                required=False,
            ),
        ],
        responses={
            200: ClassCommentSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        serializer_class = ClassCommentSerializer
        class_id = request.query_params.get('class_id')
        sender_id = request.query_params.get('sender_id')

        filters = {}
        if class_id:
            filters["class_id"] = class_id
        if sender_id:
            filters["sender_id"] = sender_id

        comments = ClassComment.objects.filter(**filters)
        serializer = serializer_class(comments, many=True)
        return Response(serializer.data)