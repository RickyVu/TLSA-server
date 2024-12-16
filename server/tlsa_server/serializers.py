from rest_framework import serializers
from .models import TLSA_User
from django.contrib.auth.hashers import make_password

class TLSAUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLSA_User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'profile_picture']

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    profile_picture = serializers.ImageField(required=False)

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        user = TLSA_User.objects.create_user(**validated_data)
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

class UserInfoPatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    password = serializers.CharField(write_only=True, required=False)
    phone_number = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = TLSA_User
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'profile_picture']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)