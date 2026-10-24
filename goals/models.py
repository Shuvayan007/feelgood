from django.conf import settings
from django.db import models


class LifeDirection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='life_directions'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title


class Goal(models.Model):
    class Category(models.TextChoices):
        CAREER = 'career', 'Career'
        FITNESS = 'fitness', 'Fitness'
        FINANCE = 'finance', 'Finance'
        LIFESTYLE = 'lifestyle', 'Lifestyle'
        PERSONAL_DEV = 'personal_dev', 'Personal Development'
        RELATIONSHIPS = 'relationships', 'Relationships'

    class TimeHorizon(models.TextChoices):
        SHORT = 'short', 'Short-term'
        MEDIUM = 'medium', 'Medium-term'
        LONG = 'long', 'Long-term'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        PAUSED = 'paused', 'Paused'
        COMPLETED = 'completed', 'Completed'
        ABANDONED = 'abandoned', 'Abandoned'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals'
    )
    life_direction = models.ForeignKey(
        LifeDirection, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='goals'
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    time_horizon = models.CharField(max_length=10, choices=TimeHorizon.choices)
    target_date = models.DateField(null=True, blank=True)
    success_criteria = models.JSONField(default=list)
    baseline = models.JSONField(null=True, blank=True)
    weekly_time_budget_hours = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    progress_pct = models.IntegerField(default=0)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        return self.title


class Milestone(models.Model):
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name='milestones'
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, default='pending')
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return self.title


class Action(models.Model):
    class ActionType(models.TextChoices):
        ONE_TIME = 'one_time', 'One-time'
        RECURRING = 'recurring', 'Recurring'

    milestone = models.ForeignKey(
        Milestone, on_delete=models.CASCADE, related_name='actions'
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    action_type = models.CharField(max_length=15, choices=ActionType.choices)
    frequency = models.CharField(max_length=30, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, default='pending')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['due_date', 'created_at']

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GoalRevision(models.Model):
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name='revisions'
    )
    field_changed = models.CharField(max_length=50)
    old_value = models.JSONField()
    new_value = models.JSONField()
    reason = models.TextField()
    revised_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-revised_at']

    def __str__(self):
        return f'{self.goal.title}: {self.field_changed}'
