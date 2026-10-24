from rest_framework import serializers
from .models import Conversation, Message, Proposal


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'tool_calls', 'tool_results', 'tokens_used', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'purpose', 'summary', 'started_at',
            'last_message_at', 'is_active', 'message_count',
        ]
        read_only_fields = ['id', 'started_at', 'last_message_at']

    def get_message_count(self, obj):
        return obj.messages.count()


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = [
            'id', 'proposal_type', 'payload', 'status',
            'user_edits', 'created_at', 'resolved_at',
        ]
        read_only_fields = ['id', 'created_at']
