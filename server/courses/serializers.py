from rest_framework import serializers
from .models import Course, CourseEnrollment, CourseClass
from tlsa_server.models import TLSA_User
from classes.models import Class

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'course_sequence', 'department', 'name']

class CoursePatchSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(max_length=8, required=True)  # Required to locate the course
    course_sequence = serializers.CharField(max_length=5, required=True)  # Required to locate the course

    class Meta:
        model = Course
        fields = ['course_code', 'course_sequence', 'name', 'department']
        extra_kwargs = {
            'name': {'required': False},
            'department': {'required': False},
        }

    def validate(self, data):
        course_code = data.get('course_code')
        course_sequence = data.get('course_sequence')

        try:
            course = Course.objects.get(course_code=course_code, course_sequence=course_sequence)
        except Course.DoesNotExist:
            raise serializers.ValidationError(f"Course with code {course_code} and sequence {course_sequence} does not exist.")

        return data

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student_user_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    course_code = serializers.CharField(write_only=True)
    course_sequence = serializers.CharField(write_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['student_user_ids', 'course_code', 'course_sequence']

    def validate_student_user_ids(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Must include at least 1 Student user_id.")
        for student_user_id in value:
            try:
                user = TLSA_User.objects.get(user_id=student_user_id)
                if user.role != "student":
                    raise serializers.ValidationError(f"User with user_id {student_user_id} is not a student.")
            except TLSA_User.DoesNotExist:
                raise serializers.ValidationError(f"User with user_id {student_user_id} does not exist.")
        return value

    def validate(self, data):
        course_code = data.get('course_code')
        course_sequence = data.get('course_sequence')

        try:
            course = Course.objects.get(course_code=course_code, course_sequence=course_sequence)
        except Course.DoesNotExist:
            raise serializers.ValidationError(f"Course with code {course_code} and sequence {course_sequence} does not exist.")

        return data

    def save(self):
        student_user_ids = self.validated_data['student_user_ids']
        course_code = self.validated_data['course_code']
        course_sequence = self.validated_data['course_sequence']
        course = Course.objects.get(course_code=course_code, course_sequence=course_sequence)
        enrollments = []
        for student_user_id in student_user_ids:
            student = TLSA_User.objects.get(user_id=student_user_id)
            enrollment = CourseEnrollment.objects.create(
                student=student,
                course=course,
            )
            enrollments.append(enrollment)
        return enrollments
    
class CourseClassSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(source='class_instance.id', write_only=True)
    course_code = serializers.CharField(source='course.course_code', write_only=True)
    course_sequence = serializers.CharField(source='course.course_sequence', write_only=True)

    class Meta:
        model = CourseClass
        fields = ['class_id', 'course_code', 'course_sequence']

    def create(self, validated_data):
        class_id = validated_data.pop('class_instance')['id']
        course = validated_data.pop('course')
        course_code = course['course_code']
        course_sequence = course['course_sequence']
        class_instance = Class.objects.get(id=class_id)
        course = Course.objects.get(course_code=course_code, course_sequence=course_sequence)
        return CourseClass.objects.create(
            class_instance=class_instance,
            course=course,
        )