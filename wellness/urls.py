from django.urls import path

from . import views

app_name = 'wellness_api'

urlpatterns = [
    path('records/', views.WellnessRecordListCreateView.as_view(), name='record-list'),
    path('records/<int:pk>/', views.WellnessRecordDetailView.as_view(), name='record-detail'),
    path('summary/', views.WellnessSummaryView.as_view(), name='summary'),
]
