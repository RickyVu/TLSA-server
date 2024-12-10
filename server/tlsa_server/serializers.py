from rest_framework import serializers
from .models import TLSA_User

class TLSAUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLSA_User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)