from rest_framework import serializers
from .models import Lab, ManageLab
from tlsa_server.models import TLSA_User

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['lab_id', 'name', 'location']

    lab_id = serializers.IntegerField(source='id', read_only=True)

class ManageLabSerializer(serializers.ModelSerializer):
    manager_id = serializers.IntegerField(source='manager.id')
    lab_id = serializers.IntegerField(source='lab.id')

    class Meta:
        model = ManageLab
        fields = ['manager_id', 'lab_id']

    def create(self, validated_data):
        manager_id = validated_data.pop('manager')['id']
        lab_id = validated_data.pop('lab')['id']
        manager = TLSA_User.objects.get(id=manager_id)
        lab = Lab.objects.get(id=lab_id)
        return ManageLab.objects.create(manager=manager, lab=lab)
    
class ManagerDetailSerializer(serializers.ModelSerializer):
    manager_id = serializers.IntegerField(source='manager.id')
    manager_name = serializers.CharField(source='manager.username')
    manager_email = serializers.EmailField(source='manager.email')
    lab_id = serializers.IntegerField(source='lab.id')

    class Meta:
        model = ManageLab
        fields = ['manager_id', 'manager_name', 'manager_email', 'lab_id']