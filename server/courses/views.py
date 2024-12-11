from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, CourseEnrollmentSerializer, CourseClassSerializer, CoursePatchSerializer
from tlsa_server.permissions import IsAuthenticated, IsTeacher
from classes.models import (TeachClass, ClassLocation)
from labs.models import (ManageLab)
from courses.models import (CourseClass)

class CourseView(APIView):
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]

    @permission_classes([IsAuthenticated])
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

        if personal and personal.lower() == "true":
            filters.update(self._get_personal_courses_filters(user))

        courses = Course.objects.filter(**filters)
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data)

    def _get_personal_courses_filters(self, user):
        filters = {}
        if user.role == "student":
            enrolled_courses = CourseEnrollment.objects.filter(student=user).values_list('course_id', flat=True)
            filters["id__in"] = enrolled_courses
        elif user.role == "teacher":
            taught_classes = TeachClass.objects.filter(teacher_id=user).values_list('class_id', flat=True)
            taught_courses = CourseClass.objects.filter(class_instance_id__in=taught_classes).values_list('course_id', flat=True)
            filters["id__in"] = taught_courses
        elif user.role == "manager":
            managed_labs = ManageLab.objects.filter(manager=user).values_list('lab_id', flat=True)
            managed_classes = ClassLocation.objects.filter(lab_id__in=managed_labs).values_list('class_id', flat=True)
            managed_courses = CourseClass.objects.filter(class_instance_id__in=managed_classes).values_list('course_id', flat=True)
            filters["id__in"] = managed_courses
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
        course_id = request.data.get('id')
        try:
            course_instance = Course.objects.get(id=course_id)
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