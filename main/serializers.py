from rest_framework import serializers
from .models import CalorieLog, SelfCheckLog
from django.contrib.auth import get_user_model

# Assuming UserProfile is the model for user
User = get_user_model()

class CalorieLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalorieLog
        fields = ['id','user','meal_type', 'calories', 'date']  # Exclude the `user` field


class SelfCheckLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfCheckLog
        fields = ['id', 'user', 'category', 'photo', 'date']
