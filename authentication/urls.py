from django.urls import path, include
from rest_framework import routers

from authentication.views import RegisterView, LoginView, Timechamp

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tt/', Timechamp.as_view(), name='timechamp'),
    ]