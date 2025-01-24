from django.urls import path
from . import views
from .views import DietPlanListView, QuestionListView, UserAnswerCreateView


urlpatterns = [
    # Other API paths
    path('dashboard/<int:user_id>/', views.DashboardData.as_view(), name='dashboard_data'),
    path('calorie-log/', views.calorie_log, name='calorie_log'),
    path('self-check-log/', views.self_check_log, name='self_check_log'),
    # path('questions/', views.QuestionViewSet.as_view(),name="questions"),
    # path('questions/', views.get_questions, name="questions",)

    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('user-answers/', UserAnswerCreateView.as_view(), name='user-answer-create'),
    path('diet-plans/', DietPlanListView.as_view(), name='diet-plan-list'), 

]