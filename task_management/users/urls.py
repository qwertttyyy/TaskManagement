from .views import UserRegistrationView
from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view()),
    path('users/auth/token/', views.obtain_auth_token),
]
