from .views import UserRegistrationView
from django.urls import path


urlpatterns = [
    path('users/register/', UserRegistrationView.as_view()),
]
