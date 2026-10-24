from django.urls import path

from . import views

app_name = 'goals_api'

urlpatterns = [
    path('', views.GoalListCreateView.as_view(), name='goal-list'),
    path('<int:pk>/', views.GoalDetailView.as_view(), name='goal-detail'),
    path(
        '<int:goal_id>/milestones/',
        views.MilestoneListCreateView.as_view(),
        name='milestone-list',
    ),
    path(
        '<int:goal_id>/milestones/<int:pk>/',
        views.MilestoneDetailView.as_view(),
        name='milestone-detail',
    ),
    path(
        'milestones/<int:milestone_id>/actions/',
        views.ActionListCreateView.as_view(),
        name='action-list',
    ),
]
