from rest_framework import serializers
from .models import Lab, ManageLab
from tlsa_server.models import TLSA_User

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['lab_id', 'name', 'location', 'safety_equipments', 'safety_notes', 'lab_image', 'map_image']

    lab_id = serializers.IntegerField(source='id', read_only=True)

class ManageLabSerializer(serializers.ModelSerializer):
    manager_user_id = serializers.CharField(source='manager.user_id')
    lab_id = serializers.IntegerField(source='lab.id')

    class Meta:
        model = ManageLab
        fields = ['manager_user_id', 'lab_id']

    def create(self, validated_data):
        manager_user_id = validated_data.pop('manager')['user_id']
        lab_id = validated_data.pop('lab')['id']
        manager = TLSA_User.objects.get(user_id=manager_user_id)
        lab = Lab.objects.get(id=lab_id)
        return ManageLab.objects.create(manager=manager, lab=lab)
    
class ManagerDetailSerializer(serializers.ModelSerializer):
    manager_user_id = serializers.CharField(source='manager.user_id')
    manager_name = serializers.CharField(source='manager.real_name')
    manager_phone = serializers.CharField(source='manager.phone_number')
    manager_email = serializers.EmailField(source='manager.email')
    lab_id = serializers.IntegerField(source='lab.id')

    class Meta:
        model = ManageLab
        fields = ['manager_user_id', 'manager_name', 'manager_phone', 'manager_email', 'lab_id']

class LabGetSerializer(serializers.ModelSerializer):
    managers = serializers.SerializerMethodField()

    class Meta:
        model = Lab
        fields = ['id', 'name', 'location', 'safety_equipments', 'safety_notes', 'lab_image', 'map_image', 'managers']

    def get_managers(self, obj):
        manage_labs = ManageLab.objects.filter(lab=obj)
        return ManagerDetailSerializer(manage_labs, many=True).data
    
class LabPatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Lab
        fields = ['id', 'name', 'location', 'safety_equipments', 'safety_notes', 'lab_image', 'map_image']