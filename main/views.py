from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CalorieLog, SelfCheckLog
from .serializers import CalorieLogSerializer, SelfCheckLogSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model



# Assuming you're using CustomUser for your user model
User = get_user_model()

# CalorieLog Create and List API
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def calorie_log(request):
    if request.method == 'POST':
        serializer = CalorieLogSerializer(data=request.data)
        if serializer.is_valid():
            # Set the user to the currently authenticated user
            serializer.save(user=request.user)
            return Response({"message":"Meal Type created Successfully!","results":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        calorie_logs = CalorieLog.objects.filter(user=request.user)
        serializer = CalorieLogSerializer(calorie_logs, many=True)
        return Response({"calorie_log":serializer.data}, status=status.HTTP_200_OK)


# SelfCheckLog Create and List API
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def self_check_log(request):
#     if request.method == 'POST':
#         serializer = SelfCheckLogSerializer(data=request.data)
#         if serializer.is_valid():
#             # Set the user to the currently authenticated user
#             serializer.save(user=request.user)
#             return Response({"message":"Selfcheck log created Successfully!","results":serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'GET':
#         self_check_logs = SelfCheckLog.objects.filter(user=request.user)
#         serializer = SelfCheckLogSerializer(self_check_logs, many=True)
#         return Response({"self_check_log":serializer.data}, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import SelfCheckLog
from .serializers import SelfCheckLogSerializer
import base64
from django.core.files.base import ContentFile
from django.conf import settings

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def self_check_log(request):
    if request.method == 'POST':
        # Check if the photo is base64 encoded
        photo_data = request.data.get('photo', None)

        if photo_data:
            # Check if the data is in base64 format
            if photo_data.startswith('data:image'):
                # Split the string to get the base64 data and file extension
                format, imgstr = photo_data.split(';base64,')
                ext = format.split('/')[1]  # Get image extension

                # Decode the base64 string and create a file-like object
                image = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)

                # Create the self-check log with the decoded image
                serializer = SelfCheckLogSerializer(data=request.data)
                if serializer.is_valid():
                    # Add the decoded image to the serializer
                    serializer.save(user=request.user, photo=image)
                    return Response({"message": "Selfcheck log created successfully!", "results": serializer.data}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid image data format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No photo data provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        self_check_logs = SelfCheckLog.objects.filter(user=request.user)
        serializer = SelfCheckLogSerializer(self_check_logs, many=True)
        return Response({"self_check_log": serializer.data}, status=status.HTTP_200_OK)



from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CalorieLog, SelfCheckLog
from .serializers import CalorieLogSerializer, SelfCheckLogSerializer
from rest_framework import status

class DashboardData(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, user_id):
        # Check if the authenticated user is the same as the user_id in the request.
        if request.user.id != int(user_id):
            return Response({"detail": "You do not have permission to view this data."}, status=status.HTTP_403_FORBIDDEN)
        
        # Fetch the most recent 30 calorie logs and self-check logs
        calorie_logs = CalorieLog.objects.filter(user_id=user_id).order_by('-date')[:30]
        self_check_logs = SelfCheckLog.objects.filter(user_id=user_id).order_by('-date')[:30]
        recommendations = [
        "Drink at least 2 liters of water daily",
        "Eat more protein-rich foods",
        "Exercise regularly for 30 minutes",
        "Track your calorie intake for better results",
    ]

        # Serialize the data
        calorie_logs_serializer = CalorieLogSerializer(calorie_logs, many=True)
        self_check_logs_serializer = SelfCheckLogSerializer(self_check_logs, many=True)

        # Return the response
        return Response({"recommendations":recommendations,
            "calorie_logs": calorie_logs_serializer.data,
            "self_check_logs": self_check_logs_serializer.data
        })
