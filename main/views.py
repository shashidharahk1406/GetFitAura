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

from rest_framework import viewsets
from .models import Question
from .serializers import QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('id')  # Order questions by ID for consistent presentation
    serializer_class = QuestionSerializer




# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Question
# from .serializers import QuestionSerializer

# @api_view(['GET'])
# def get_questions(request):
#     permission_classes = [IsAuthenticated] 
#     questions = Question.objects.all()
#     serializer = QuestionSerializer(questions, many=True)
#     return Response(serializer.data)


from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer

class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer





from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Question, Option, UserAnswer, DietPlan, DietPlanItem
from .serializers import QuestionSerializer, UserAnswerSerializer, DietPlanSerializer
# from .diet_plan_logic import generate_diet_plan

# class UserAnswerCreateView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserAnswerSerializer

#     def create(self, request, *args, **kwargs):
#         user_answers_data = request.data

#         try:
#             user_answers = []
#             for answer_data in user_answers_data:
#                 question_id = answer_data.get('questionId')
#                 option_id = answer_data.get('optionId')

#                 if not question_id or not option_id:
#                     return Response({"error": "Invalid answer format."}, status=400)

#                 try:
#                     question = Question.objects.get(id=question_id)
#                     option = Option.objects.get(id=option_id, question=question)
#                     user_answer = UserAnswer(user=request.user, question=question, option=option)
#                     user_answers.append(user_answer)
#                 except Question.DoesNotExist:
#                     return Response({"error": f"Question with ID {question_id} not found."}, status=400)
#                 except Option.DoesNotExist:
#                     return Response({"error": f"Option with ID {option_id} not found for question {question_id}."}, status=400)

#             UserAnswer.objects.bulk_create(user_answers)

#             # Generate diet plan
#             diet_plan = generate_diet_plan(user_answers) 

#             # Create DietPlan and DietPlanItem objects
#             diet_plan_instance = DietPlan.objects.create(user=request.user)
#             for meal_time, food_items in diet_plan.items():
#                 for food_item in food_items:
#                     DietPlanItem.objects.create(
#                         diet_plan=diet_plan_instance,
#                         meal_time=meal_time,
#                         food_item=food_item['name'],
#                         description=food_item['description']
#                     )

#             serializer = DietPlanSerializer(diet_plan_instance)
#             return Response(serializer.data, status=201)
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)






class UserAnswerCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAnswerSerializer

    def create(self, request, *args, **kwargs):
        user_answers_data = request.data

        try:
            user_answers = []
            for answer_data in user_answers_data:
                question_id = answer_data.get('questionId')
                option_id = answer_data.get('optionId')

                if not question_id or not option_id:
                    return Response({"error": "Invalid answer format."}, status=400)

                try:
                    question = Question.objects.get(id=question_id)
                    option = Option.objects.get(id=option_id, question=question)

                    user_answer, created = UserAnswer.objects.get_or_create(
                        user=request.user, 
                        question=question, 
                        defaults={'option': option} 
                    ) 
                    user_answers.append(user_answer) 

                except Question.DoesNotExist:
                    return Response({"error": f"Question with ID {question_id} not found."}, status=400)
                except Option.DoesNotExist:
                    return Response({"error": f"Option with ID {option_id} not found for question {question_id}."}, status=400)

            # Generate diet plan
            diet_plan = generate_diet_plan(user_answers) 

            # Create DietPlan and DietPlanItem objects
            diet_plan_instance = DietPlan.objects.create(user=request.user)

            for meal_time, food_items in diet_plan.items():
                for food_item in food_items:
                    # Check if a DietPlanItem with the same meal_time and food_item already exists
                    existing_item = DietPlanItem.objects.filter(
                        diet_plan=diet_plan_instance,
                        meal_time=meal_time,
                        food_item=food_item['name']
                    ).first()

                    if not existing_item:
                        DietPlanItem.objects.create(
                            diet_plan=diet_plan_instance,
                            meal_time=meal_time,
                            food_item=food_item['name'],
                            description=food_item['description']
                        )

            serializer = DietPlanSerializer(diet_plan_instance)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class DietPlanListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DietPlanSerializer

    def get_queryset(self):
        return DietPlan.objects.filter(user=self.request.user)

# diet_plan_logic.py
from .models import UserAnswer, Question

def generate_diet_plan(user_answers):
    """
    Generates a basic diet plan based on user answers.

    This is a simplified example and needs to be further enhanced with 
    more complex logic based on your specific requirements.

    Args:
        user_answers: A list of UserAnswer objects.

    Returns:
        A dictionary representing the diet plan, with keys for each meal time 
        and values as lists of food items.
    """

    diet_plan = {}

    # Example: Simplified logic based on a few questions 
    exercise_frequency = None
    fruit_vegetable_intake = None

    for answer in user_answers:
        if answer.question.question_text == "How often do you exercise in a week?": 
            if answer.option.option_text == "4-5 times":
                exercise_frequency = "Active"

        if answer.question.question_text == "How often do you eat fruits and vegetables?":
            if answer.option.option_text == "Daily":
                fruit_vegetable_intake = "High"

    if exercise_frequency == "Active" and fruit_vegetable_intake == "High":
        diet_plan = {
            "morning_breakfast": [
                {"name": "Oatmeal with berries and nuts", "description": ""},
                {"name": "Yogurt with fruit and granola", "description": ""}
            ],
            "lunch": [
                {"name": "Grilled chicken salad", "description": ""},
                {"name": "Lentil soup with whole-grain bread", "description": ""}
            ],
            "dinner": [
                {"name": "Salmon with roasted vegetables", "description": ""},
                {"name": "Vegetarian stir-fry with brown rice", "description": ""}
            ],
            "snacks": [
                {"name": "Fruit and nuts", "description": ""},
                {"name": "Greek yogurt", "description": ""}
            ]
        }
    else:
        # Default diet plan 
        diet_plan = {
            "morning_breakfast": [
                {"name": "Scrambled eggs with whole-grain toast", "description": ""},
                {"name": "Smoothie with fruit and spinach", "description": ""}
            ],
            "lunch": [
                {"name": "Tuna salad sandwich on whole-grain bread", "description": ""},
                {"name": "Chicken or vegetable stir-fry with brown rice", "description": ""}
            ],
            "dinner": [
                {"name": "Grilled chicken or fish with roasted vegetables", "description": ""},
                {"name": "Lentil soup with whole-grain bread", "description": ""}
            ],
            "snacks": [
                {"name": "Apple with almond butter", "description": ""},
                {"name": "Greek yogurt with berries", "description": ""}
            ]
        }

    return diet_plan
