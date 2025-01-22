from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from rest_framework_simplejwt.tokens import RefreshToken


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'email', 'password', 'blood_group', 'age', 'gender')

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
#         user = User.objects.filter(email=email).first()

#         if user and user.check_password(password):
#             return {'user': user}
#         raise serializers.ValidationError("Invalid credentials")

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()






# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser

# Using the CustomUser model
User = CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'blood_group', 'age', 'gender')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Make sure to hash the password
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()
        

        if user and user.check_password(password):  # Check the hashed password
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")
