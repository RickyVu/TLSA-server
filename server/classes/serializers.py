from rest_framework import serializers
from .models import Class, TeachClass, ClassLocation, ClassComment, Experiment, ExperimentFile, ExperimentImage
from django.contrib.auth import get_user_model

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['class_id', 'name', 'start_time']

    class_id = serializers.IntegerField(source='id', read_only=True)

class TeachClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachClass
        fields = ['class_id', 'teacher_id']

    teacher_id = serializers.CharField(source='teacher_id.user_id')

    def create(self, validated_data):
        user_id = validated_data.pop('teacher_id')["user_id"]

        user_model = get_user_model()
        try:
            teacher = user_model.objects.get(user_id=user_id)
        except user_model.DoesNotExist:
            raise serializers.ValidationError({"teacher_id": "Invalid user_id. TLSA_User does not exist."})

        teach_class = TeachClass.objects.create(
            teacher_id=teacher,
            **validated_data
        )
        return teach_class

class ClassLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassLocation
        fields = ['class_id', 'lab_id']

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
        return [{'teacher_id': teacher.teacher_id.id, "teacher_name": teacher.teacher_id.real_name} for teacher in teachers]
    
class ClassPatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'start_time', 'created_at', 'updated_at']

class ClassCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ClassComment
        fields = ['id', 'sender_id', 'class_id', 'content', 'sent_time']

    sender_id = serializers.CharField(source='sender_id.user_id', read_only=True)

class ClassCommentWithoutSenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassComment
        fields = ['class_id', 'content']


# -----------------------------------------------
# Experiment

class ExperimentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentImage
        fields = ['image']

class ExperimentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentFile
        fields = ['file']

class ExperimentSerializer(serializers.ModelSerializer):
    class_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    images = ExperimentImageSerializer(many=True, read_only=True)
    files = ExperimentFileSerializer(many=True, read_only=True)

    class Meta:
        model = Experiment
        fields = [
            'id', 'title', 'estimated_time', 'safety_tags', 'experiment_method_tags',
            'submission_type_tags', 'other_tags', 'description', 'class_id', 'images', 'files'
        ]
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'safety_tags': {'required': False, 'allow_null': True, 'default': []},
            'submission_type_tags': {'required': False, 'allow_null': True, 'default': []},
            'estimated_time': {'required': False, 'default': 0},
            'experiment_method_tags': {'required': False, 'allow_null': True, 'default': []},
            'other_tags': {'required': False, 'allow_null': True, 'default': []},
        }

class ExperimentPatchSerializer(serializers.ModelSerializer):
    class_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), required=False)
    images = ExperimentImageSerializer(many=True, read_only=True)
    files = ExperimentFileSerializer(many=True, read_only=True)

    class Meta:
        model = Experiment
        fields = [
            'id', 'title', 'estimated_time', 'safety_tags', 'experiment_method_tags',
            'submission_type_tags', 'other_tags', 'description', 'class_id', 'images', 'files'
        ]
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'safety_tags': {'required': False, 'allow_null': True, 'default': []},
            'submission_type_tags': {'required': False, 'allow_null': True, 'default': []},
            'estimated_time': {'required': False, 'default': 0},
            'experiment_method_tags': {'required': False, 'allow_null': True, 'default': []},
            'other_tags': {'required': False, 'allow_null': True, 'default': []},
        }