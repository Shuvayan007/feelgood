from django.conf import settings
from django.db import models


class Habit(models.Model):
    class Frequency(models.TextChoices):
        DAILY = 'daily', 'Daily'
        WEEKLY = 'weekly', 'Weekly'
        CUSTOM = 'custom', 'Custom'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits'
    )
    goal = models.ForeignKey(
        'goals.Goal', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='linked_habits'
    )
    title = models.CharField(max_length=200)
    frequency = models.CharField(max_length=10, choices=Frequency.choices)
    target_count = models.IntegerField(default=1)
    days_of_week = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class HabitLog(models.Model):
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name='logs'
    )
    logged_date = models.DateField()
    count = models.IntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['habit', 'logged_date']
        ordering = ['-logged_date']
        indexes = [
            models.Index(fields=['habit', 'logged_date']),
        ]

    def __str__(self):
        return f'{self.habit.title} — {self.logged_date}'
