from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'email', 'blood_group', 'age', 'gender')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('blood_group', 'gender')

admin.site.register(CustomUser, UserProfileAdmin)
