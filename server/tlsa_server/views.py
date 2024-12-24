from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from .serializers import (TLSAUserSerializer, 
                          UserRegistrationSerializer, 
                          StaffRegistrationSerializer, 
                          UserLoginSerializer, 
                          RefreshTokenSerializer, 
                          UserInfoPatchSerializer)
from .permissions import IsTeachingAffairs

class RegisterView(APIView):
    """Register a new user."""
    serializer_class = UserRegistrationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeachingAffairs()]
        return []

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "real_name": {"type": "string"},
                    "user_id": {"type": "string"},
                    "password": {"type": "string"},
                    "profile_picture": {"type": "string", "format": "binary"},
                    "phone_number": {"type": "string"},
                    "department": {"type": "string"},
                },
            }
        },
        examples=[
            OpenApiExample(
                "Example Registration",
                description="Example of a registration request.",
                value={
                    "real_name": "student",
                    "user_id": "2021000000",
                    "password": "securepassword123",
                    "profile_picture": "file.png",
                    "phone_number": "18000000000",
                    "department": "Computer Science",
                },
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            password = serializer.validated_data['password']
            real_name = serializer.validated_data.get('real_name')
            profile_picture = serializer.validated_data.get('profile_picture')
            phone_number = serializer.validated_data.get('phone_number')
            department = serializer.validated_data.get('department')

            User = get_user_model()
            if User.objects.filter(user_id=user_id).exists():
                return Response({"error": "User ID already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = User(
                real_name=real_name,
                user_id=user_id,
                profile_picture=profile_picture,
                phone_number=phone_number,
                department=department,
                role="student"  # Default role for new users
            )
            user.set_password(password)
            user.save()

            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterStaffView(APIView):
    """Register a new staff user (teacher or manager)."""
    serializer_class = StaffRegistrationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeachingAffairs()]
        return []

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "real_name": {"type": "string"},
                    "user_id": {"type": "string"},
                    "password": {"type": "string"},
                    "profile_picture": {"type": "string", "format": "binary"},
                    "phone_number": {"type": "string"},
                    "department": {"type": "string"},
                    "role": {"type": "string", "enum": ["teacher", "manager"]},  # Role parameter
                },
            }
        },
        examples=[
            OpenApiExample(
                "Example Staff Registration",
                description="Example of a staff registration request.",
                value={
                    "real_name": "teacher",
                    "user_id": "2021000001",
                    "password": "securepassword123",
                    "profile_picture": "file.png",
                    "phone_number": "18000000000",
                    "department": "Computer Science",
                    "role": "teacher",  # Role parameter
                },
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            password = serializer.validated_data['password']
            real_name = serializer.validated_data.get('real_name')
            profile_picture = serializer.validated_data.get('profile_picture')
            phone_number = serializer.validated_data.get('phone_number')
            department = serializer.validated_data.get('department')
            role = serializer.validated_data.get('role')

            if role not in ["teacher", "manager"]:
                return Response({"error": "Invalid role. Role must be either 'teacher' or 'manager'."}, status=status.HTTP_400_BAD_REQUEST)

            User = get_user_model()
            if User.objects.filter(user_id=user_id).exists():
                return Response({"error": "User ID already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = User(
                real_name=real_name,
                user_id=user_id,
                profile_picture=profile_picture,
                phone_number=phone_number,
                department=department,
                role=role  # Set the role based on the request
            )
            user.set_password(password)
            user.save()

            return Response({"message": "Staff user registered successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """Login user and return JWT tokens."""

    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id')
            password = request.data.get('password')

            User = get_user_model()
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid user ID or password."}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                return Response({"error": "Invalid user ID or password."}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role,
                'user_id': user.user_id
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    """Retrieve user information based on user_id."""
    authentication_classes = [JWTAuthentication]
    serializer_class = TLSAUserSerializer

    def get_permissions(self):
        # IMPORTANT: GET method may have additional user role behaviours defined
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return []

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='User ID to retrieve information for',
                required=False,
            ),
            OpenApiParameter(
                name='role',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter users by role (student/teacher/manager)',
                required=False,
            ),
        ],
        responses={
            200: TLSAUserSerializer(many=True),
            404: None,
            403: None,
        },
    )
    def get(self, request):
        user_id = request.query_params.get('user_id')
        role = request.query_params.get('role')

        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if role:
            filters["role"] = role

        User = get_user_model()
        users = User.objects.filter(**filters)

        # Check if the requesting user is allowed to view the information
        if request.user.role in ['teacher', 'manager', 'student', 'teachingAffairs']:
            serializer = self.serializer_class(users, many=True)
            return Response(serializer.data)
        elif request.user.role == 'student':
            if user_id and request.user.user_id == user_id:
                serializer = self.serializer_class(users, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "You do not have permission to view this user's information."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "You do not have permission to view this user's information."}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        request=UserInfoPatchSerializer,
    )
    def patch(self, request, format=None):
        user_id = request.data.get('user_id')
        User = get_user_model()
        try:
            user_instance = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is allowed to update the user information
        if request.user.role in ['teacher', 'manager', 'teachingAffairs'] or request.user.user_id == user_id:
            serializer = UserInfoPatchSerializer(user_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "User information updated successfully.",
                        "user": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to update this user's information."}, status=status.HTTP_403_FORBIDDEN)
        
class ChangeUserRoleView(APIView):
    """Change user role."""
    authentication_classes = [JWTAuthentication]
    serializer_class = TLSAUserSerializer

    def get_permissions(self):
        # IMPORTANT: GET method may have additional user role behaviours defined
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            return [IsTeachingAffairs()]
        return []

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=str,
                location=OpenApiParameter.QUERY,
                description='User ID to retrieve information for',
                required=False,
            ),
            OpenApiParameter(
                name='role',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter users by role (student/teacher/manager)',
                required=False,
            ),
        ],
        responses={
            200: TLSAUserSerializer(many=True),
            404: None,
            403: None,
        },
    )
    def get(self, request):
        user_id = request.query_params.get('user_id')
        role = request.query_params.get('role')

        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if role:
            filters["role"] = role

        User = get_user_model()
        users = User.objects.filter(**filters)

        # Check if the requesting user is allowed to view the information
        if request.user.role in ['teacher', 'manager', 'student', 'teachingAffairs']:
            serializer = self.serializer_class(users, many=True)
            return Response(serializer.data)
        elif request.user.role == 'student':
            if user_id and request.user.user_id == user_id:
                serializer = self.serializer_class(users, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "You do not have permission to view this user's information."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "You do not have permission to view this user's information."}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        request=UserInfoPatchSerializer,
    )
    def patch(self, request, format=None):
        user_id = request.data.get('user_id')
        User = get_user_model()
        try:
            user_instance = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is allowed to update the user information
        if request.user.role in ['teacher', 'manager'] or request.user.user_id == user_id:
            serializer = UserInfoPatchSerializer(user_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "User information updated successfully.",
                        "user": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to update this user's information."}, status=status.HTTP_403_FORBIDDEN)

class ValidateTokenView(APIView):
    """Validate a JWT token."""

    def post(self, request):
        token = request.data.get('token')
        try:
            # Validate the token
            token_obj = AccessToken(token)
            return Response({"valid": True, "user_id": token_obj['user_id']})
        except TokenError:
            return Response({"valid": False}, status=status.HTTP_401_UNAUTHORIZED)
        
class RefreshTokenView(APIView):
    """Refresh access token using refresh token."""

    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            refresh = serializer.validated_data['refresh']

            try:
                # Create a token object from the refresh token string
                token = RefreshToken(refresh)

                # Generate a new access token
                new_access = str(token.access_token)

                return Response({
                    'access': new_access,
                })
            except TokenError:
                return Response({"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(APIView):
    """Verify the current user's token."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Token is valid."})