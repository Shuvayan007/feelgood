from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Goal, Milestone, Action
from .serializers import (
    GoalSerializer, GoalCreateSerializer,
    MilestoneSerializer, ActionSerializer,
)


# ── API Views ────────────────────────────────────────────────────


class GoalListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GoalCreateSerializer
        return GoalSerializer

    def get_queryset(self):
        qs = Goal.objects.filter(user=self.request.user)
        if s := self.request.query_params.get('status'):
            qs = qs.filter(status=s)
        if c := self.request.query_params.get('category'):
            qs = qs.filter(category=c)
        return qs.prefetch_related('milestones__actions')


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user
        ).prefetch_related('milestones__actions')

    def perform_destroy(self, instance):
        instance.status = Goal.Status.ABANDONED
        instance.save(update_fields=['status', 'updated_at'])


class MilestoneListCreateView(ListCreateAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Milestone.objects.filter(
            goal_id=self.kwargs['goal_id'],
            goal__user=self.request.user,
        ).prefetch_related('actions')

    def perform_create(self, serializer):
        goal = get_object_or_404(
            Goal, pk=self.kwargs['goal_id'], user=self.request.user
        )
        serializer.save(goal=goal)


class MilestoneDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Milestone.objects.filter(
            goal_id=self.kwargs['goal_id'],
            goal__user=self.request.user,
        ).prefetch_related('actions')


class ActionListCreateView(ListCreateAPIView):
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Action.objects.filter(
            milestone_id=self.kwargs['milestone_id'],
            milestone__goal__user=self.request.user,
        )

    def perform_create(self, serializer):
        milestone = get_object_or_404(
            Milestone,
            pk=self.kwargs['milestone_id'],
            goal__user=self.request.user,
        )
        serializer.save(milestone=milestone)


# ── Frontend Views ───────────────────────────────────────────────


@login_required
def goals_list_view(request):
    goals = Goal.objects.filter(user=request.user).prefetch_related(
        'milestones__actions'
    )
    grouped = {
        'active': goals.filter(status=Goal.Status.ACTIVE),
        'draft': goals.filter(status=Goal.Status.DRAFT),
        'paused': goals.filter(status=Goal.Status.PAUSED),
        'completed': goals.filter(status=Goal.Status.COMPLETED),
    }
    return render(request, 'goals/list.html', {
        'grouped_goals': grouped,
        'total_count': goals.count(),
    })


@login_required
def goal_detail_view(request, pk):
    goal = get_object_or_404(
        Goal.objects.prefetch_related('milestones__actions', 'revisions'),
        pk=pk,
        user=request.user,
    )
    return render(request, 'goals/detail.html', {'goal': goal})
