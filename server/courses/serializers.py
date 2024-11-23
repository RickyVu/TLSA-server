from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'name']

    course_id = serializers.IntegerField(source='id', read_only=True)