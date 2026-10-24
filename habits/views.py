from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    CreateAPIView, ListAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer


# ── API Views ────────────────────────────────────────────────────


class HabitListCreateView(ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(
            user=self.request.user
        ).prefetch_related('logs')


class HabitDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitLogView(CreateAPIView):
    serializer_class = HabitLogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = get_object_or_404(
            Habit, pk=self.kwargs['habit_id'], user=self.request.user
        )
        serializer.save(habit=habit)


class HabitHistoryView(ListAPIView):
    serializer_class = HabitLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HabitLog.objects.filter(
            habit_id=self.kwargs['habit_id'],
            habit__user=self.request.user,
        )


# ── Frontend Views ───────────────────────────────────────────────


@login_required
def habits_view(request):
    habits = Habit.objects.filter(
        user=request.user, is_active=True
    ).prefetch_related('logs')
    return render(request, 'habits/list.html', {'habits': habits})
