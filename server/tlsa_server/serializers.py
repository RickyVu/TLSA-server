from rest_framework import serializers
from .models import TLSA_User
from django.contrib.auth.hashers import make_password

class TLSAUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLSA_User
        fields = ['id', 'username', 'email', 'role']

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

class UserInfoPatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = TLSA_User
        fields = ['id', 'username', 'email', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)