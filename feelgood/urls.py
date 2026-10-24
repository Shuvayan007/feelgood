from django.contrib import admin
from django.urls import path, include

from core.views import (
    index_view, dashboard_view, login_view, register_view,
    logout_view, profile_view, ProfileAPIView, DashboardAPIView,
)
from mentor.views import chat_view, onboarding_view
from goals.views import goals_list_view, goal_detail_view
from habits.views import habits_view
from finance.views import finance_view
from wellness.views import wellness_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── API ──────────────────────────────────────────────────────
    path('api/auth/', include('core.urls')),
    path('api/profile/', ProfileAPIView.as_view(), name='api_profile'),
    path('api/dashboard/', DashboardAPIView.as_view(), name='api_dashboard'),
    path('api/mentor/', include('mentor.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/habits/', include('habits.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/wellness/', include('wellness.urls')),
    path('api/memory/', include('memory.urls')),

    # ── Frontend ─────────────────────────────────────────────────
    path('', index_view, name='index'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('onboarding/', onboarding_view, name='onboarding'),
    path('chat/', chat_view, name='chat'),
    path('chat/<int:conversation_id>/', chat_view, name='chat_conversation'),
    path('goals/', goals_list_view, name='goals_list'),
    path('goals/<int:pk>/', goal_detail_view, name='goal_detail'),
    path('habits/', habits_view, name='habits'),
    path('finance/', finance_view, name='finance'),
    path('wellness/', wellness_view, name='wellness'),
]
