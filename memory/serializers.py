from rest_framework import serializers

from .models import MemoryEntry, ConversationSummary


class MemoryEntrySerializer(serializers.ModelSerializer):
    memory_type_display = serializers.CharField(
        source='get_memory_type_display', read_only=True
    )

    class Meta:
        model = MemoryEntry
        fields = [
            'id', 'memory_type', 'memory_type_display', 'content',
            'structured_data', 'is_user_verified', 'created_at', 'expires_at',
        ]
        read_only_fields = ['id', 'created_at']


class ConversationSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationSummary
        fields = [
            'id', 'conversation', 'summary_text', 'key_decisions',
            'facts_extracted', 'messages_covered_from',
            'messages_covered_to', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
