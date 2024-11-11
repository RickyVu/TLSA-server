from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, RefreshTokenSerializer

class RegisterView(APIView):
    """Register a new user."""
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            User = get_user_model()
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = User(username=username)
            user.set_password(password)
            user.role = "student"
            user.save()

            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Login user and return JWT tokens."""

    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')

            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.get(username=username)

            if not user.check_password(password):
                return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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