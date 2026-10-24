from django.contrib import admin

from .models import LifeDirection, Goal, Milestone, Action, GoalRevision


@admin.register(LifeDirection)
class LifeDirectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'user', 'category', 'status', 'progress_pct',
        'target_date', 'updated_at',
    ]
    list_filter = ['status', 'category', 'time_horizon']
    search_fields = ['title', 'description']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal', 'status', 'target_date', 'sort_order']
    list_filter = ['status']
    search_fields = ['title']


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['title', 'milestone', 'action_type', 'status', 'due_date']
    list_filter = ['action_type', 'status']
    search_fields = ['title']


@admin.register(GoalRevision)
class GoalRevisionAdmin(admin.ModelAdmin):
    list_display = ['goal', 'field_changed', 'revised_at']
    list_filter = ['field_changed']
