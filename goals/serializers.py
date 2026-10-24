from rest_framework import serializers

from .models import LifeDirection, Goal, Milestone, Action, GoalRevision


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = [
            'id', 'title', 'description', 'action_type', 'frequency',
            'due_date', 'status', 'completed_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class MilestoneSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(many=True, read_only=True)

    class Meta:
        model = Milestone
        fields = [
            'id', 'title', 'description', 'target_date', 'status',
            'sort_order', 'completed_at', 'created_at', 'actions',
        ]
        read_only_fields = ['id', 'created_at']


class GoalSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, read_only=True)
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )

    class Meta:
        model = Goal
        fields = [
            'id', 'life_direction', 'title', 'description', 'category',
            'category_display', 'time_horizon', 'target_date',
            'success_criteria', 'baseline', 'weekly_time_budget_hours',
            'progress_pct', 'status', 'status_display',
            'created_at', 'updated_at', 'milestones',
        ]
        read_only_fields = ['id', 'progress_pct', 'created_at', 'updated_at']


class GoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            'title', 'description', 'category', 'time_horizon',
            'target_date', 'success_criteria', 'baseline',
            'weekly_time_budget_hours', 'life_direction',
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class LifeDirectionSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = LifeDirection
        fields = [
            'id', 'title', 'description', 'priority', 'is_active',
            'created_at', 'goals',
        ]
        read_only_fields = ['id', 'created_at']


class GoalRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalRevision
        fields = [
            'id', 'field_changed', 'old_value', 'new_value',
            'reason', 'revised_at',
        ]
        read_only_fields = ['id', 'revised_at']
