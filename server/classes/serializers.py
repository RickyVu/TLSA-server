from rest_framework import serializers
from .models import Class

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['class_id', 'name', 'start_time']

    class_id = serializers.IntegerField(source='id', read_only=True)