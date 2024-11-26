from rest_framework import serializers
from .models import Lab

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['lab_id', 'name', 'location']

    lab_id = serializers.IntegerField(source='id', read_only=True)
    manager = serializers.ListField(child=serializers.CharField(), read_only=True)