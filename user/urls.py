from django.urls import path
from .views import SignupView, LoginView, ForgotPasswordView, ResetPasswordView,RefreshTokenView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
     path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
]
    