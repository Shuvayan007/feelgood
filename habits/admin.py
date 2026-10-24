from django.contrib import admin

from .models import Habit, HabitLog


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'frequency', 'target_count', 'is_active', 'created_at']
    list_filter = ['frequency', 'is_active']
    search_fields = ['title']


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['habit', 'logged_date', 'count']
    list_filter = ['logged_date']
