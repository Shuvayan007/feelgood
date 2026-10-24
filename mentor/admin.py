from django.contrib import admin
from .models import Conversation, Message, Proposal


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'purpose', 'is_active', 'started_at', 'last_message_at']
    list_filter = ['purpose', 'is_active']
    search_fields = ['user__email']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'short_content', 'created_at']
    list_filter = ['role']

    def short_content(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    short_content.short_description = 'Content'


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['user', 'proposal_type', 'status', 'created_at', 'resolved_at']
    list_filter = ['proposal_type', 'status']
    search_fields = ['user__email']
