from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from tlsa_server.permissions import IsAuthenticated, IsTeacher, IsTeachingAffairs, IsManager
from .models import (Class, 
                     TeachClass, 
                     ClassLocation, 
                     ClassComment,
                     Experiment,
                     ExperimentImage,
                     ExperimentFile)
from .serializers import (ClassSerializer, 
                          TeachClassSerializer, 
                          ClassLocationSerializer,
                          ClassOutputSerializer,
                          ClassPatchSerializer,
                          ClassCommentSerializer, 
                          ClassCommentWithoutSenderSerializer, 
                          ExperimentSerializer, 
                          ExperimentPatchSerializer,
                          ExperimentImageSerializer,
                          ExperimentFileSerializer)
from django.db.models import Q
from courses.models import (CourseClass, CourseEnrollment)
from labs.models import (ManageLab)

class ClassView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ClassSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [(IsTeacher|IsTeachingAffairs)()]
        elif self.request.method == 'PATCH':
            return [(IsTeacher|IsTeachingAffairs)()]
        elif self.request.method == 'DELETE':
            return [(IsTeacher|IsTeachingAffairs)()]
        return []

    @extend_schema(
        request=ClassSerializer,
    )
    def post(self, request, format=None):
        serializer_class = ClassSerializer
        serializer = serializer_class(data=request.data)
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

        query = Q()

        if class_id:
            query &= Q(id=class_id)
        if class_name:
            query &= Q(name__icontains=class_name)
        if course_id:
            query &= Q(courseclass__course_id=course_id)

        if personal and personal.lower() == "true":
            if user.role == "student":
                enrolled_courses = CourseEnrollment.objects.filter(student=user).values_list('course_id', flat=True)
                query &= Q(courseclass__course_id__in=enrolled_courses)
            elif user.role == "teacher":
                query &= Q(teachclass__teacher_id=user)
            elif user.role == "manager":
                managed_labs = ManageLab.objects.filter(manager=user).values_list('lab_id', flat=True)
                query &= Q(classlocation__lab_id__in=managed_labs)

        classes = Class.objects.filter(query)

        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=ClassPatchSerializer,
    )
    def patch(self, request, format=None):
        class_id = request.data.get('id')
        try:
            class_instance = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({"message": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClassPatchSerializer(class_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Class updated successfully.",
                    "class": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='class_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Class ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Class deleted",
                value={"message": "Class deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Class not found",
                value={"message": "Class not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        """
        Delete a class.
        """
        class_id = request.query_params.get('class_id')
        try:
            class_instance = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({"message": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

        class_instance.delete()
        return Response({"message": "Class deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class TeacherClassView(APIView):
    serializer_class = TeachClassSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            return [(IsTeacher|IsTeachingAffairs)()]
        elif self.request.method == 'DELETE':
            return [(IsTeacher|IsTeachingAffairs)()]
        return []

    @extend_schema(
        request=TeachClassSerializer,
    )
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
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='class_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Class ID to delete teacher assignment',
                required=True,
            ),
            OpenApiParameter(
                name='teacher_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Teacher ID to delete assignment',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Assignment deleted",
                value={"message": "Teacher assignment deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Assignment not found",
                value={"message": "Teacher assignment not found."},
                response_only=True,
            ),
            400: OpenApiExample(
                name="Missing parameters",
                value={"message": "Both class_id and teacher_id are required to delete an assignment."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        class_id = request.query_params.get('class_id')
        teacher_id = request.query_params.get('teacher_id')

        if not class_id or not teacher_id:
            return Response(
                {"message": "Both class_id and teacher_id are required to delete an assignment."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            assignment = TeachClass.objects.get(class_id=class_id, teacher_id=teacher_id)
        except TeachClass.DoesNotExist:
            return Response({"message": "Teacher assignment not found."}, status=status.HTTP_404_NOT_FOUND)

        assignment.delete()
        return Response({"message": "Teacher assignment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class ClassLocationView(APIView):
    serializer_class = ClassLocationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [(IsTeacher|IsTeachingAffairs)()]
        elif self.request.method == 'DELETE':
            return [(IsTeacher|IsTeachingAffairs)()]
        return []

    @extend_schema(
        request=ClassLocationSerializer,
    )
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
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='class_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Class ID to delete location',
                required=True,
            ),
            OpenApiParameter(
                name='lab_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Lab ID to delete location',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Location deleted",
                value={"message": "Location deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Location not found",
                value={"message": "Location not found."},
                response_only=True,
            ),
            400: OpenApiExample(
                name="Missing parameters",
                value={"message": "Both class_id and lab_id are required to delete a location."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        class_id = request.query_params.get('class_id')
        lab_id = request.query_params.get('lab_id')

        if not class_id or not lab_id:
            return Response(
                {"message": "Both class_id and lab_id are required to delete a location."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            location = ClassLocation.objects.get(class_id=class_id, lab_id=lab_id)
        except ClassLocation.DoesNotExist:
            return Response({"message": "Location not found."}, status=status.HTTP_404_NOT_FOUND)

        location.delete()
        return Response({"message": "Location deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class CommentToClassView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return []
    
    @extend_schema(
        request=ClassCommentWithoutSenderSerializer,
    )
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
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='comment_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Comment ID to delete comment',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Comment deleted",
                value={"message": "Comment deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Comment not found",
                value={"message": "Comment not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        user = request.user
        comment_id = request.query_params.get('comment_id')
        if not comment_id:
            return Response(
                {"message": "Comment ID is required to delete a comment."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            comment = ClassComment.objects.get(id=comment_id)
        except ClassComment.DoesNotExist:
            return Response({"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.role not in ["teacher", "manager", "teachingAffairs"]:
            if user != comment.sender_id:
                return Response({"error": "You do not have permission to delete another user's message."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
# -----------------------------------------------
# Experiment

class ExperimentView(APIView):
    serializer_class = ExperimentSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [(IsTeacher|IsManager|IsTeachingAffairs)()]
        elif self.request.method == 'PATCH':
            return [(IsTeacher|IsManager|IsTeachingAffairs)()]
        elif self.request.method == 'DELETE':
            return [(IsTeacher|IsManager|IsTeachingAffairs)()]
        return []

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "estimated_time": {"type": "number"},
                    "safety_tags": {"type": "array", "items": {"type": "string"}},
                    "experiment_method_tags": {"type": "array", "items": {"type": "string"}},
                    "submission_type_tags": {"type": "array", "items": {"type": "string"}},
                    "other_tags": {"type": "array", "items": {"type": "string"}},
                    "description": {"type": "string"},
                    "class_id": {"type": "integer"},
                    "images": {"type": "array", "items": {"type": "string", "format": "binary"}},
                    "files": {"type": "array", "items": {"type": "string", "format": "binary"}},
                },
            }
        },
        examples=[
            OpenApiExample(
                "Example Request",
                description="Example of a request to partially update an experiment with images and files.",
                value={
                    "id": 1,
                    "title": "Updated Experiment Title",
                    "description": "Updated description of the experiment.",
                    "images": ["image1.jpg", "image2.jpg"],
                    "files": ["instructions.pdf", "data_sheet.xlsx"],
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request, format=None):
        experiment_serializer = ExperimentSerializer(data=request.data)
        if experiment_serializer.is_valid():
            experiment = experiment_serializer.save()

            images = request.FILES.getlist('images')
            for image in images:
                ExperimentImage.objects.create(experiment=experiment, image=image)

            files = request.FILES.getlist('files')
            for file in files:
                ExperimentFile.objects.create(experiment=experiment, file=file)

            return Response(
                {
                    "message": "Experiment created successfully.",
                    "experiment": experiment_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(experiment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='experiment_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Query by experiment_id',
                required=False,
            ),
            OpenApiParameter(
                name='class_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Filter by class_id',
                required=False,
            ),
            OpenApiParameter(
                name='description',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Query by description (similarity)',
                required=False,
            ),
            OpenApiParameter(
                name='safety_tag',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter by safety tag (similarity)',
                required=False,
            ),
        ],
        responses={
            200: ExperimentSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        serializer_class = ExperimentSerializer
        experiment_id = request.query_params.get('experiment_id')
        class_id = request.query_params.get('class_id')
        description = request.query_params.get('description')
        safety_tag = request.query_params.get('safety_tag')

        experiments = Experiment.objects.all()

        if experiment_id:
            experiments = experiments.filter(id=experiment_id)
        if class_id:
            experiments = experiments.filter(class_id=class_id)
        if description:
            experiments = experiments.filter(description__icontains=description)
        if safety_tag:
            experiments = experiments.filter(safety_tags__icontains=safety_tag)

        serializer = serializer_class(experiments, many=True)
        return Response(serializer.data)

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "estimated_time": {"type": "number"},
                    "safety_tags": {"type": "array", "items": {"type": "string"}},
                    "experiment_method_tags": {"type": "array", "items": {"type": "string"}},
                    "submission_type_tags": {"type": "array", "items": {"type": "string"}},
                    "other_tags": {"type": "array", "items": {"type": "string"}},
                    "description": {"type": "string"},
                    "class_id": {"type": "integer"},
                    "images": {"type": "array", "items": {"type": "string", "format": "binary"}},
                    "files": {"type": "array", "items": {"type": "string", "format": "binary"}},
                },
            }
        },
        examples=[
            OpenApiExample(
                "Example Request",
                description="Example of a request to partially update an experiment with images and files.",
                value={
                    "id": 1,
                    "title": "Updated Experiment Title",
                    "description": "Updated description of the experiment.",
                    "images": ["image1.jpg", "image2.jpg"],
                    "files": ["instructions.pdf", "data_sheet.xlsx"],
                },
                request_only=True,
            ),
        ],
    )
    def patch(self, request, format=None):
        experiment_id = request.data.get('id')
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Experiment.DoesNotExist:
            return Response({"message": "Experiment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExperimentPatchSerializer(experiment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            images = request.FILES.getlist('images')
            for image in images:
                ExperimentImage.objects.create(experiment=experiment, image=image)

            files = request.FILES.getlist('files')
            for file in files:
                ExperimentFile.objects.create(experiment=experiment, file=file)

            return Response(
                {
                    "message": "Experiment updated successfully.",
                    "experiment": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='experiment_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Experiment ID to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Experiment deleted",
                value={"message": "Experiment deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Experiment not found",
                value={"message": "Experiment not found."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        experiment_id = request.query_params.get('experiment_id')
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Experiment.DoesNotExist:
            return Response({"message": "Experiment not found."}, status=status.HTTP_404_NOT_FOUND)

        experiment.delete()
        return Response({"message": "Experiment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)