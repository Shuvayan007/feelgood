from django.conf import settings
from django.db import models


class MemoryEntry(models.Model):
    class MemoryType(models.TextChoices):
        FACT = 'fact', 'Fact'
        PREFERENCE = 'preference', 'Preference'
        CONSTRAINT = 'constraint', 'Constraint'
        REFLECTION = 'reflection', 'Reflection'
        DECISION = 'decision', 'Decision'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='memory_entries'
    )
    memory_type = models.CharField(max_length=15, choices=MemoryType.choices)
    content = models.TextField()
    structured_data = models.JSONField(null=True, blank=True)
    source_conversation = models.ForeignKey(
        'mentor.Conversation', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='extracted_memories'
    )
    is_user_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'memory entries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'memory_type']),
        ]

    def __str__(self):
        return f'{self.memory_type}: {self.content[:60]}'


class ConversationSummary(models.Model):
    conversation = models.ForeignKey(
        'mentor.Conversation', on_delete=models.CASCADE,
        related_name='summaries'
    )
    summary_text = models.TextField()
    key_decisions = models.JSONField(default=list)
    facts_extracted = models.JSONField(default=list)
    messages_covered_from = models.IntegerField()
    messages_covered_to = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'conversation summaries'
        ordering = ['-created_at']

    def __str__(self):
        return f'Summary for conversation {self.conversation_id}'
