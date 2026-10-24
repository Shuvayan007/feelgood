from django.urls import path

from . import views

app_name = 'habits_api'

urlpatterns = [
    path('', views.HabitListCreateView.as_view(), name='habit-list'),
    path('<int:pk>/', views.HabitDetailView.as_view(), name='habit-detail'),
    path(
        '<int:habit_id>/log/',
        views.HabitLogView.as_view(),
        name='habit-log',
    ),
    path(
        '<int:habit_id>/history/',
        views.HabitHistoryView.as_view(),
        name='habit-history',
    ),
]
