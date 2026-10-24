from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='api_register'),
    path('login/', views.LoginView.as_view(), name='api_login'),
    path('logout/', views.LogoutView.as_view(), name='api_logout'),
    path('refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
