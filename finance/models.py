from django.conf import settings
from django.db import models


class ExpenseCategory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='expense_categories'
    )
    name = models.CharField(max_length=100)
    is_discretionary = models.BooleanField(default=True)
    monthly_budget = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    icon = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name_plural = 'expense categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class FinancialRecord(models.Model):
    class RecordType(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'
        SAVINGS = 'savings', 'Savings'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='financial_records'
    )
    category = models.ForeignKey(
        ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='records'
    )
    record_type = models.CharField(max_length=10, choices=RecordType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    description = models.CharField(max_length=300, blank=True)
    recorded_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'recorded_date']),
            models.Index(fields=['user', 'record_type', 'recorded_date']),
        ]

    def __str__(self):
        return f'{self.record_type} {self.amount} {self.currency}'


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='budgets'
    )
    category = models.ForeignKey(
        ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='budgets'
    )
    month = models.DateField()
    planned_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month']

    def __str__(self):
        label = self.category.name if self.category else 'Total'
        return f'{label} budget — {self.month:%Y-%m}'
