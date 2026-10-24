from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WellnessRecord
from .serializers import WellnessRecordSerializer


# ── API Views ────────────────────────────────────────────────────


class WellnessRecordListCreateView(ListCreateAPIView):
    serializer_class = WellnessRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = WellnessRecord.objects.filter(user=self.request.user)
        if rt := self.request.query_params.get('record_type'):
            qs = qs.filter(record_type=rt)
        return qs


class WellnessRecordDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = WellnessRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WellnessRecord.objects.filter(user=self.request.user)


class WellnessSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        period = request.query_params.get('period', 'month')
        today = date.today()

        if period == 'week':
            start = today - timedelta(days=today.weekday())
        else:
            start = today.replace(day=1)

        qs = WellnessRecord.objects.filter(
            user=request.user, recorded_date__gte=start,
        )

        if rt := request.query_params.get('record_type'):
            qs = qs.filter(record_type=rt)

        summary = list(
            qs.values('record_type')
            .annotate(count=Count('id'), latest_date=Max('recorded_date'))
            .order_by('record_type')
        )

        return Response({
            'period': period,
            'start_date': start.isoformat(),
            'summary': summary,
        })


# ── Frontend Views ───────────────────────────────────────────────


@login_required
def wellness_view(request):
    records = WellnessRecord.objects.filter(user=request.user)[:50]
    return render(request, 'wellness/overview.html', {'records': records})
