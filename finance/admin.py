from django.contrib import admin

from .models import ExpenseCategory, FinancialRecord, Budget


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_discretionary', 'monthly_budget']
    list_filter = ['is_discretionary']
    search_fields = ['name']


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = [
        'description', 'user', 'record_type', 'amount', 'currency',
        'category', 'recorded_date',
    ]
    list_filter = ['record_type', 'currency', 'recorded_date']
    search_fields = ['description']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'month', 'planned_amount']
    list_filter = ['month']
