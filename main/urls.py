from django.urls import path
from . import views

urlpatterns = [
    # Other API paths
    path('dashboard/<int:user_id>/', views.DashboardData.as_view(), name='dashboard_data'),
    path('calorie-log/', views.calorie_log, name='calorie_log'),
    path('self-check-log/', views.self_check_log, name='self_check_log'),
]