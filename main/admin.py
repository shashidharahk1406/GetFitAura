from django.contrib import admin

# Register your models here.
from .models import CalorieLog, SelfCheckLog,Question,Option
admin.site.register(CalorieLog)
admin.site.register(SelfCheckLog)
admin.site.register(Question)
admin.site.register(Option)




