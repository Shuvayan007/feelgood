from rest_framework import serializers

from .models import ExpenseCategory, FinancialRecord, Budget


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'is_discretionary', 'monthly_budget', 'icon']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FinancialRecordSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name', read_only=True, default=None
    )

    class Meta:
        model = FinancialRecord
        fields = [
            'id', 'category', 'category_name', 'record_type', 'amount',
            'currency', 'description', 'recorded_date', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'category', 'month', 'planned_amount', 'created_at']
        read_only_fields = ['id', 'created_at']


class FinanceSummarySerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_savings = serializers.DecimalField(max_digits=14, decimal_places=2)
    by_category = serializers.ListField(child=serializers.DictField())
