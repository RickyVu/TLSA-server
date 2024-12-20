from rest_framework import serializers
from .models import TLSA_User, numeric_validator
from django.contrib.auth.hashers import make_password

class TLSAUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLSA_User
        fields = ['user_id', 'email', 'role', 'phone_number', 'profile_picture', 'real_name', 'department']
    
class UserRegistrationSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    profile_picture = serializers.ImageField(required=False)
    real_name = serializers.CharField(required=False)
    user_id = serializers.CharField(required=True, validators=[numeric_validator])
    phone_number = serializers.CharField(required=False)
    department = serializers.CharField(required=False, max_length=50)

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        real_name = validated_data.pop('real_name', None)
        department = validated_data.pop('department', None)
        phone_number = validated_data.pop('phone_number', None)
        user_id = validated_data.pop('user_id')

        user = TLSA_User.objects.create_user(
            username=user_id,
            user_id=user_id,
            password=validated_data['password'],
            real_name=real_name,
            profile_picture=profile_picture,
            phone_number=phone_number,
            department=department,
            role="student"  # Default role for new users
        )

        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    
class UserInfoPatchSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=False)
    phone_number = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)
    real_name = serializers.CharField(required=False)
    department = serializers.CharField(required=False, max_length=50)

    class Meta:
        model = TLSA_User
        fields = ['user_id', 'email', 'password', 'phone_number', 'profile_picture', 'real_name', 'department']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)