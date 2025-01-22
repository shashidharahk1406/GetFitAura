from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CalorieLog, SelfCheckLog

admin.site.register(CalorieLog)
admin.site.register(SelfCheckLog)


