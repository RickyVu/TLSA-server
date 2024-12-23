from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, CourseEnrollmentSerializer, CourseClassSerializer, CoursePatchSerializer, CourseEnrollmentGetSerializer
from tlsa_server.permissions import IsAuthenticated, IsTeacher
from classes.models import (TeachClass, ClassLocation)
from labs.models import (ManageLab)
from courses.models import (CourseClass)


class CourseView(APIView):
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]

    @permission_classes([IsAuthenticated])
    def get(self, request, format=None):
        course_code = request.query_params.get('course_code')
        course_sequence = request.query_params.get('course_sequence')
        course_name = request.query_params.get('course_name')
        personal = request.query_params.get('personal')
        user = request.user

        filters = {}
        if course_code:
            filters["course_code"] = course_code
        if course_sequence:
            filters["course_sequence"] = course_sequence
        if course_name:
            filters["name__icontains"] = course_name

        if personal and personal.lower() == "true":
            filters.update(self._get_personal_courses_filters(user))

        courses = Course.objects.filter(**filters)
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)

    def _get_personal_courses_filters(self, user):
        filters = {}
        if user.role == "student":
            enrolled_courses = CourseEnrollment.objects.filter(student=user).values_list('course__course_code', 'course__course_sequence')
            filters["course_code__in"], filters["course_sequence__in"] = zip(*enrolled_courses)
        elif user.role == "teacher":
            taught_classes = TeachClass.objects.filter(teacher_id=user).values_list('class_id', flat=True)
            taught_courses = CourseClass.objects.filter(class_instance_id__in=taught_classes).values_list('course__course_code', 'course__course_sequence')
            filters["course_code__in"], filters["course_sequence__in"] = zip(*taught_courses)
        elif user.role == "manager":
            managed_labs = ManageLab.objects.filter(manager=user).values_list('lab_id', flat=True)
            managed_classes = ClassLocation.objects.filter(lab_id__in=managed_labs).values_list('class_id', flat=True)
            managed_courses = CourseClass.objects.filter(class_instance_id__in=managed_classes).values_list('course__course_code', 'course__course_sequence')
            filters["course_code__in"], filters["course_sequence__in"] = zip(*managed_courses)
        return filters

    @permission_classes([IsTeacher])
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

    @permission_classes([IsTeacher])
    @extend_schema(
        request=CoursePatchSerializer,
    )
    def patch(self, request, format=None):
        course_code = request.data.get('course_code')
        course_sequence = request.data.get('course_sequence')

        # Locate the course using the composite key
        try:
            course_instance = Course.objects.get(course_code=course_code, course_sequence=course_sequence)
        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CoursePatchSerializer(course_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Course updated successfully.",
                    "course": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsTeacher])
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='course_code',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Course code to delete',
                required=True,
            ),
            OpenApiParameter(
                name='course_sequence',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Course sequence to delete',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Course deleted",
                value={"message": "Course deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Course not found",
                value={"message": "Course not found."},
                response_only=True,
            ),
            400: OpenApiExample(
                name="Missing parameters",
                value={"message": "course_code and course_sequence are required to delete a course."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        course_code = request.query_params.get('course_code')
        course_sequence = request.query_params.get('course_sequence')

        if not course_code or not course_sequence:
            return Response(
                {"message": "course_code and course_sequence are required to delete a course."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(course_code=course_code, course_sequence=course_sequence)
        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        course.delete()
        return Response({"message": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class CourseEnrollmentView(APIView):
    serializer_class = CourseEnrollmentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        return []

    @extend_schema(
        request=CourseEnrollmentSerializer,
        responses={
            201: OpenApiExample(
                name="Enrollment Success",
                value={
                    "message": "Students enrolled successfully.",
                    "enrollment": {
                        "student_user_ids": ["2021000000", "2021000001"],
                        "course_id": 1
                    }
                },
                response_only=True,
            ),
            400: OpenApiExample(
                name="Validation Error",
                value={
                    "student_user_ids": ["User with user_id 2021000000 does not exist."]
                },
                response_only=True,
            ),
        },
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            enrollments = serializer.save()
            return Response(
                {
                    "message": "Students enrolled successfully.",
                    "enrollment": {
                        "student_user_ids": [enrollment.student.user_id for enrollment in enrollments],
                        "course_id": enrollments[0].course.id
                    }
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
                description='Course ID to retrieve enrolled students for',
                required=False,
            ),
        ],
        responses={
            200: CourseEnrollmentGetSerializer(many=True),
        },
    )
    def get(self, request, format=None):
        course_id = request.query_params.get('course_id')

        filters = {}
        if course_id:
            filters["course_id"] = course_id

        enrollments = CourseEnrollment.objects.filter(**filters)
        print(enrollments)

        serializer = CourseEnrollmentGetSerializer(enrollments, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='student_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Student ID to delete enrollment',
                required=True,
            ),
            OpenApiParameter(
                name='course_code',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Course code to delete enrollment',
                required=True,
            ),
            OpenApiParameter(
                name='course_sequence',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Course sequence to delete enrollment',
                required=True,
            ),
        ],
        responses={
            204: OpenApiExample(
                name="Enrollment deleted",
                value={"message": "Course enrollment deleted successfully."},
                response_only=True,
            ),
            404: OpenApiExample(
                name="Enrollment not found",
                value={"message": "Course enrollment not found."},
                response_only=True,
            ),
            400: OpenApiExample(
                name="Missing parameters",
                value={"message": "student_id, course_code, and course_sequence are required to delete an enrollment."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        student_id = request.query_params.get('student_id')
        course_code = request.query_params.get('course_code')
        course_sequence = request.query_params.get('course_sequence')

        if not student_id or not course_code or not course_sequence:
            return Response(
                {"message": "student_id, course_code, and course_sequence are required to delete an enrollment."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            enrollment = CourseEnrollment.objects.get(
                student__user_id=student_id,
                course__course_code=course_code,
                course__course_sequence=course_sequence
            )
        except CourseEnrollment.DoesNotExist:
            return Response({"message": "Course enrollment not found."}, status=status.HTTP_404_NOT_FOUND)

        enrollment.delete()
        return Response({"message": "Course enrollment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='course_code',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Course code to delete class from',
                required=True,
            ),
            OpenApiParameter(
                name='course_sequence',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Course sequence to delete class from',
                required=True,
            ),
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
                value={"message": "Not found."},
                response_only=True,
            ),
            400: OpenApiExample(
                name="Missing parameters",
                value={"message": "course_code, course_sequence, and class_id are required to delete a class."},
                response_only=True,
            ),
        },
    )
    def delete(self, request, format=None):
        course_code = request.query_params.get('course_code')
        course_sequence = request.query_params.get('course_sequence')
        class_id = request.query_params.get('class_id')

        if not course_code or not course_sequence or not class_id:
            return Response(
                {"message": "course_code, course_sequence, and class_id are required to delete a class."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(course_code=course_code, course_sequence=course_sequence)
        except Course.DoesNotExist:
            return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            course_class = CourseClass.objects.get(course=course, id=class_id)
        except CourseClass.DoesNotExist:
            return Response({"message": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

        course_class.delete()
        return Response({"message": "Class deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
