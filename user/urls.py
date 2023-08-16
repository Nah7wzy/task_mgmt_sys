from django.contrib import admin
from django.urls import path
from .views import SignupView, LoginView, UserPublicAPIView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/<str:pk>/', UserPublicAPIView.as_view(), name='user-public')
]
