from django.db import models

# Create your models here.

from django.contrib.auth.models import User  # Assuming you're using the default User model, else use CustomUser
from django.conf import settings
from django.contrib.postgres.fields import JSONField  # Import JSONField from django.contrib.postgres

class CalorieLog(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking to User model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)  # Automatically sets the date when a log is created
    meal_type = models.CharField(max_length=10, choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')])  # Meal type options
    calories = models.IntegerField()  # Calories for the meal
    
    def __str__(self):
        return f"{self.user.username}'s Calorie Log on {self.date}"

class SelfCheckLog(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking to User model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=[('face', 'Face'), ('body', 'Body'), ('food', 'Food')])  # Type of self-check
    photo = models.ImageField(upload_to='uploads/')  # Image upload for the self-check
    date = models.DateField(auto_now_add=True)  # Automatically sets the date when the log is created
    
    def __str__(self):
        return f"{self.user.username}'s Self Check in {self.category} on {self.date}"
    






# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     option_a = models.CharField(max_length=100)
#     option_b = models.CharField(max_length=100)
#     option_c = models.CharField(max_length=100)
#     option_d = models.CharField(max_length=100)
#     # Removed 'correct_answer' as it's not relevant for diet plan questions 

#     def __str__(self):
#         return self.question_text

class Question(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=100)

    def __str__(self):
        return self.option_text



# class UserAnswer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     option = models.ForeignKey(Option, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('user', 'question') 

# # Create a DietPlan model to store the generated diet plans
# class DietPlan(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     plan_name = models.CharField(max_length=255, default='Generated Diet Plan') 
#     created_at = models.DateTimeField(auto_now_add=True)

# class DietPlanItem(models.Model):
#     diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name='items')
#     meal_time = models.CharField(max_length=50)  # e.g., "Breakfast", "Lunch", "Dinner", "Snack"
#     food_item = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True) 



class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question') 

class DietPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=255, default='Generated Diet Plan') 
    created_at = models.DateTimeField(auto_now_add=True)

class DietPlanItem(models.Model):
    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name='items')
    meal_time = models.CharField(max_length=50)  # e.g., "Breakfast", "Lunch", "Dinner", "Snack"
    food_item = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) 


from django.db import models
from django.contrib.postgres.fields import JSONField 
from django.db.models import JSONField

# class DietPlanItem(models.Model):
#     diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE, related_name='items')
#     meal_time = models.CharField(max_length=50)  # e.g., "Breakfast", "Lunch", "Dinner", "Snack"
#     food_items = JSONField() 