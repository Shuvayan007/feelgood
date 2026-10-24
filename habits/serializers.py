from rest_framework import serializers

from .models import Habit, HabitLog


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['id', 'logged_date', 'count', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class HabitSerializer(serializers.ModelSerializer):
    current_streak = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()
    recent_logs = HabitLogSerializer(source='logs', many=True, read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'title', 'frequency', 'target_count', 'days_of_week',
            'is_active', 'goal', 'created_at',
            'current_streak', 'completion_rate', 'recent_logs',
        ]
        read_only_fields = ['id', 'created_at']

    def get_current_streak(self, obj) -> int:
        # TODO: calculate consecutive days/weeks of completion
        return 0

    def get_completion_rate(self, obj) -> float:
        # TODO: calculate completion rate over the last 30 days
        return 0.0

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
