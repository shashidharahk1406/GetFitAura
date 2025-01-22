from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    blood_group = models.CharField(max_length=5)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20)
    
    def save(self, *args, **kwargs):
        # Ensure username defaults to email if not set
        if not self.username:
            self.username = self.email
        
        # Ensure the full name is properly set if provided
        if self.first_name and self.last_name:
            self.first_name = self.first_name.title()  # Optional: Capitalize first name
            self.last_name = self.last_name.title()    # Optional: Capitalize last name
        
        # Save the model instance
        super().save(*args, **kwargs)
