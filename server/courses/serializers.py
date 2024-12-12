from rest_framework import serializers
from .models import Course, CourseEnrollment, CourseClass
from tlsa_server.models import TLSA_User
from classes.models import Class

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'name']

    course_id = serializers.IntegerField(source='id', read_only=True)

class CoursePatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Class
        fields = ['id', 'name']

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['student_ids', 'course_id']
    
    def validate_student_ids(self, value):
        if len(value)==0:
            raise serializers.ValidationError(f"Must include at least 1 Student id.")
        for student_id in value:
            try:
                user = TLSA_User.objects.get(id=student_id)
                if user.role != "student":
                    raise serializers.ValidationError(f"User with id {student_id} is not a student.")
            except TLSA_User.DoesNotExist:
                raise serializers.ValidationError(f"User with id {student_id} does not exist.")
        return value

    def validate_course_id(self, value):
        try:
            course = Course.objects.get(id=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError(f"Course with id {value} does not exist.")
        return value

    def validate(self, data):
        student_ids = data.get('student_ids')
        course_id = data.get('course_id')

        self.validate_student_ids(student_ids)
        self.validate_course_id(course_id)

        return data

    def save(self):
        student_ids = self.validated_data['student_ids']
        course_id = self.validated_data['course_id']
        course = Course.objects.get(id=course_id)
        enrollments = []
        for student_id in student_ids:
            student = TLSA_User.objects.get(id=student_id)
            enrollment = CourseEnrollment.objects.create(student=student, course=course)
            enrollments.append(enrollment)
        return enrollments

class CourseClassSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(source='class_instance.id', write_only=True)
    course_id = serializers.IntegerField(source='course.id', write_only=True)

    class Meta:
        model = CourseClass
        fields = ['class_id', 'course_id']

    def create(self, validated_data):
        class_id = validated_data.pop('class_instance')['id']
        course_id = validated_data.pop('course')['id']
        class_instance = Class.objects.get(id=class_id)
        course = Course.objects.get(id=course_id)
        return CourseClass.objects.create(class_instance=class_instance, course=course)