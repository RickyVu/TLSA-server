from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from tlsa_server.permissions import IsAuthenticated, IsTeacher
from .models import (Class,
                     TeachClass,
                     ClassLocation,
                     ClassComment)
from .serializers import (ClassSerializer,
                          TeachClassSerializer,
                          ClassLocationSerializer,
                          ClassOutputSerializer,
                          ClassPatchSerializer,
                          ClassCommentSerializer, ClassCommentWithoutSenderSerializer)
from courses.models import (CourseClass, CourseEnrollment)
from labs.models import (ManageLab)


class ClassView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ClassSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsTeacher()]
        elif self.request.method == 'PATCH':
            return [IsTeacher()]
        elif self.request.method == 'DELETE':
            return [IsTeacher()]
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

        filters = {}
        id_in_filters = None

        if class_id:
            filters["id"] = class_id
        if class_name:
            filters["name__icontains"] = class_name

        if course_id:
            course_classes = CourseClass.objects.filter(course_id=course_id).values_list('class_instance_id', flat=True)
            id_in_filters = set(course_classes) if id_in_filters is None else id_in_filters.intersection(course_classes)

        if personal and personal.lower() == "true":
            if user.role == "student":
                enrolled_courses = CourseEnrollment.objects.filter(student=user).values_list('course_id', flat=True)
                enrolled_classes = CourseClass.objects.filter(course_id__in=enrolled_courses).values_list('class_instance_id', flat=True)
                id_in_filters = set(enrolled_classes) if id_in_filters is None else id_in_filters.intersection(enrolled_classes)
            elif user.role == "teacher":
                taught_classes = TeachClass.objects.filter(teacher_id=user).values_list('class_id', flat=True)
                id_in_filters = set(taught_classes) if id_in_filters is None else id_in_filters.intersection(taught_classes)
            elif user.role == "manager":
                managed_labs = ManageLab.objects.filter(manager=user).values_list('lab_id', flat=True)
                managed_classes = ClassLocation.objects.filter(lab_id__in=managed_labs).values_list('class_id', flat=True)
                id_in_filters = set(managed_classes) if id_in_filters is None else id_in_filters.intersection(managed_classes)

        if id_in_filters is not None:
            filters["id__in"] = list(id_in_filters)

        classes = Class.objects.filter(**filters)
        serializer = self.serializer_class(classes, many=True)
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
    permission_classes = [IsAuthenticated]

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
                name='class_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Class ID to delete comment',
                required=True,
            ),
            OpenApiParameter(
                name='sender_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Sender ID to delete comment',
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
        class_id = request.query_params.get('class_id')
        sender_id = request.query_params.get('sender_id')
        if not class_id or not sender_id:
            return Response(
                {"message": "Both class_id and sender_id are required to delete a comment."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            comment = ClassComment.objects.get(class_id=class_id, sender_id=sender_id)
        except ClassComment.DoesNotExist:
            return Response({"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
