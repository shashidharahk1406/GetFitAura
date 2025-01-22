from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User  # Assuming you're using the default User model, else use CustomUser
from django.conf import settings

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
