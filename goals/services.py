from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Sum

from .models import Goal


class GoalPlanningService:
    """Application-level goal planning logic. The LLM proposes; this service validates."""

    def validate_time_budget(self, user, proposed_hours: Decimal) -> dict:
        """Check if the user has enough unallocated weekly hours for a new goal."""
        allocated = Goal.objects.filter(
            user=user, status=Goal.Status.ACTIVE,
        ).aggregate(
            total=Sum('weekly_time_budget_hours')
        )['total'] or Decimal('0')

        profile = getattr(user, 'profile', None)
        available = Decimal(str(
            getattr(profile, 'available_hours_per_week', 0) or 40
        ))
        remaining = available - allocated

        return {
            'available_total': float(available),
            'currently_allocated': float(allocated),
            'remaining': float(remaining),
            'proposed': float(proposed_hours),
            'fits': proposed_hours <= remaining,
        }

    def detect_conflicts(self, user) -> list[dict]:
        """Find goals with overlapping deadlines that exceed the user's time budget."""
        # TODO: implement full conflict detection across milestone dates
        return []

    def calculate_progress(self, goal: Goal) -> int:
        """Recalculate goal progress from milestone and action completion."""
        milestones = goal.milestones.all()
        if not milestones.exists():
            return 0

        completed = milestones.filter(status='completed').count()
        total = milestones.count()
        pct = int((completed / total) * 100)

        if goal.progress_pct != pct:
            goal.progress_pct = pct
            goal.save(update_fields=['progress_pct', 'updated_at'])

        return pct

    def detect_stalled_goals(self, user, threshold_days: int = 14) -> list[Goal]:
        """Return active goals with no progress logged in threshold_days."""
        cutoff = date.today() - timedelta(days=threshold_days)
        return list(
            Goal.objects.filter(
                user=user,
                status=Goal.Status.ACTIVE,
                updated_at__date__lt=cutoff,
            )
        )

    def generate_weekly_plan(self, user, week_start: date) -> dict:
        """Generate a proposed weekly plan balancing all active goals."""
        active_goals = Goal.objects.filter(
            user=user, status=Goal.Status.ACTIVE,
        ).prefetch_related('milestones__actions')

        # TODO: build a real scheduling algorithm factoring in
        # available hours, goal priorities, and action due dates
        plan = {
            'week_start': week_start.isoformat(),
            'goals': [],
        }
        for goal in active_goals:
            next_actions = []
            for ms in goal.milestones.filter(status='pending')[:2]:
                for action in ms.actions.filter(status='pending')[:2]:
                    next_actions.append({
                        'action_id': action.id,
                        'title': action.title,
                        'milestone': ms.title,
                    })
            plan['goals'].append({
                'goal_id': goal.id,
                'title': goal.title,
                'hours_budgeted': float(goal.weekly_time_budget_hours or 0),
                'next_actions': next_actions,
            })

        return plan
