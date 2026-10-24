from django.conf import settings
from django.db import models


class WellnessRecord(models.Model):
    class RecordType(models.TextChoices):
        WORKOUT = 'workout', 'Workout'
        MEASUREMENT = 'measurement', 'Measurement'
        NUTRITION = 'nutrition', 'Nutrition'
        SLEEP = 'sleep', 'Sleep'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='wellness_records'
    )
    goal = models.ForeignKey(
        'goals.Goal', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='wellness_records'
    )
    record_type = models.CharField(max_length=15, choices=RecordType.choices)
    data = models.JSONField()
    recorded_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'record_type', 'recorded_date']),
        ]

    def __str__(self):
        return f'{self.record_type} — {self.recorded_date}'
