from rest_framework import serializers
from .models import Class, TeachClass, ClassLocation, ClassComment

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['class_id', 'name', 'start_time']

    class_id = serializers.IntegerField(source='id', read_only=True)

class TeachClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachClass
        fields = ['class_id', 'teacher_id']

class ClassLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLocation
        fields = ['class_id', 'lab_id']

class ClassCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassComment
        fields = ['sender_id', 'class_id', 'content', 'sent_time']

class ClassCommentWithoutSenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassComment
        fields = ['class_id', 'content']