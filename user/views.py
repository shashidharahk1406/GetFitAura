from django.shortcuts import render

# Create your views here.


from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'message': 'User created successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            

            user_data = {
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'blood_group': user.blood_group,
                'age': user.age,
                'gender': user.gender,
                
            }
            return Response({'message':"Login Successful",'user_data':user_data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                # Send password reset email logic here
                return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            # Validate token and reset password logic
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

class RefreshTokenView(APIView):
    def post(self, request):
        # Extract the refresh token from the request data
        refresh_token = request.data.get('refresh', None)
        
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a refresh token object from the received token string
            refresh = RefreshToken(refresh_token)
            
            # Generate a new access token from the refresh token
            access_token = str(refresh.access_token)
            
            return Response({
                'access': access_token,
                'refresh': str(refresh)  # Optionally, return the new refresh token
            })
        except TokenError:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

