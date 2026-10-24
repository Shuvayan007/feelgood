from django.urls import path

from . import views

app_name = 'memory_api'

urlpatterns = [
    path('', views.MemoryListView.as_view(), name='memory-list'),
    path('<int:pk>/', views.MemoryDeleteView.as_view(), name='memory-delete'),
]
