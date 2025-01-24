from rest_framework import serializers
from .models import CalorieLog, DietPlan, DietPlanItem, SelfCheckLog, UserAnswer
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



from rest_framework import serializers
from .models import Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True) 

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'options'] 




class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'

# class DietPlanItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DietPlanItem
#         fields = '__all__'



# In DietPlanItemSerializer
class DietPlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlanItem
        fields = '__all__' 
        

class DietPlanSerializer(serializers.ModelSerializer):
    items = DietPlanItemSerializer(many=True, read_only=True)

    class Meta:
        model = DietPlan
        fields = '__all__'




        

