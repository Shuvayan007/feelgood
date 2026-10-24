from django.urls import path

from . import views

app_name = 'finance_api'

urlpatterns = [
    path('records/', views.FinancialRecordListCreateView.as_view(), name='record-list'),
    path('records/<int:pk>/', views.FinancialRecordDetailView.as_view(), name='record-detail'),
    path('summary/', views.FinanceSummaryView.as_view(), name='summary'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
]
