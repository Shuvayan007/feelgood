from django.contrib import admin

from .models import MemoryEntry, ConversationSummary


@admin.register(MemoryEntry)
class MemoryEntryAdmin(admin.ModelAdmin):
    list_display = ['memory_type', 'user', 'content', 'is_user_verified', 'created_at']
    list_filter = ['memory_type', 'is_user_verified']
    search_fields = ['content']


@admin.register(ConversationSummary)
class ConversationSummaryAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'messages_covered_from', 'messages_covered_to', 'created_at']
