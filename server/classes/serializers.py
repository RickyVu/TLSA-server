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

from rest_framework import serializers
from .models import Class, ClassLocation, TeachClass

class ClassOutputSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField()
    teachers = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'start_time', 'locations', 'teachers']

    def get_locations(self, obj):
        locations = ClassLocation.objects.filter(class_id=obj.id)
        return [{'lab_id': location.lab_id.id} for location in locations]

    def get_teachers(self, obj):
        teachers = TeachClass.objects.filter(class_id=obj.id)
        return [{'teacher_id': teacher.teacher_id.id, "teacher_name": teacher.teacher_id.username} for teacher in teachers]
    
class ClassPatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'start_time', 'created_at', 'updated_at']

class ClassCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassComment
        fields = ['sender_id', 'class_id', 'content', 'sent_time']

class ClassCommentWithoutSenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassComment
        fields = ['class_id', 'content']