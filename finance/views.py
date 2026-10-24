from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExpenseCategory, FinancialRecord
from .serializers import (
    ExpenseCategorySerializer, FinancialRecordSerializer,
)


# ── API Views ────────────────────────────────────────────────────


class FinancialRecordListCreateView(ListCreateAPIView):
    serializer_class = FinancialRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = FinancialRecord.objects.filter(
            user=self.request.user
        ).select_related('category')
        if rt := self.request.query_params.get('record_type'):
            qs = qs.filter(record_type=rt)
        return qs


class FinancialRecordDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FinancialRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FinancialRecord.objects.filter(user=self.request.user)


class FinanceSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        period = request.query_params.get('period', 'month')
        today = date.today()

        if period == 'week':
            start = today - timedelta(days=today.weekday())
        elif period == 'quarter':
            quarter_month = ((today.month - 1) // 3) * 3 + 1
            start = today.replace(month=quarter_month, day=1)
        else:
            start = today.replace(day=1)

        records = FinancialRecord.objects.filter(
            user=request.user, recorded_date__gte=start,
        )

        totals = records.values('record_type').annotate(total=Sum('amount'))
        summary = {'income': 0, 'expense': 0, 'savings': 0}
        for row in totals:
            summary[row['record_type']] = float(row['total'])

        by_category = list(
            records.filter(record_type='expense')
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        return Response({
            'period': period,
            'start_date': start.isoformat(),
            'total_income': summary['income'],
            'total_expenses': summary['expense'],
            'total_savings': summary['savings'],
            'by_category': [
                {'category': r['category__name'] or 'Uncategorised', 'total': float(r['total'])}
                for r in by_category
            ],
        })


class CategoryListCreateView(ListCreateAPIView):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseCategory.objects.filter(user=self.request.user)


# ── Frontend Views ───────────────────────────────────────────────


@login_required
def finance_view(request):
    records = FinancialRecord.objects.filter(
        user=request.user
    ).select_related('category')[:50]
    categories = ExpenseCategory.objects.filter(user=request.user)
    return render(request, 'finance/overview.html', {
        'records': records,
        'categories': categories,
    })
