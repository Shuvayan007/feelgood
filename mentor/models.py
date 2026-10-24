from django.conf import settings
from django.db import models


class Conversation(models.Model):
    class Purpose(models.TextChoices):
        ONBOARDING = 'onboarding', 'Onboarding'
        CHECK_IN = 'check_in', 'Check-in'
        PLANNING = 'planning', 'Planning'
        GENERAL = 'general', 'General'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations'
    )
    purpose = models.CharField(max_length=20, choices=Purpose.choices, default=Purpose.GENERAL)
    summary = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-last_message_at']

    def __str__(self):
        return f'{self.purpose} — {self.user.email} ({self.started_at:%Y-%m-%d})'


class Message(models.Model):
    class Role(models.TextChoices):
        USER = 'user', 'User'
        ASSISTANT = 'assistant', 'Assistant'
        SYSTEM = 'system', 'System'

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    role = models.CharField(max_length=10, choices=Role.choices)
    content = models.TextField()
    tool_calls = models.JSONField(null=True, blank=True)
    tool_results = models.JSONField(null=True, blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']

    def __str__(self):
        preview = self.content[:60] + '...' if len(self.content) > 60 else self.content
        return f'[{self.role}] {preview}'


class Proposal(models.Model):
    class ProposalType(models.TextChoices):
        NEW_GOAL = 'new_goal', 'New Goal'
        PLAN_REVISION = 'plan_revision', 'Plan Revision'
        WEEKLY_PLAN = 'weekly_plan', 'Weekly Plan'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        EDITED = 'edited', 'Edited'
        EXPIRED = 'expired', 'Expired'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proposals'
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.SET_NULL, null=True, blank=True
    )
    proposal_type = models.CharField(max_length=20, choices=ProposalType.choices)
    payload = models.JSONField()
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    user_edits = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'proposals'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.proposal_type} — {self.status} ({self.user.email})'
