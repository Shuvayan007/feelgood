from rest_framework import serializers

from .models import WellnessRecord


class WellnessRecordSerializer(serializers.ModelSerializer):
    record_type_display = serializers.CharField(
        source='get_record_type_display', read_only=True
    )

    class Meta:
        model = WellnessRecord
        fields = [
            'id', 'record_type', 'record_type_display', 'goal',
            'data', 'recorded_date', 'notes', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WellnessSummarySerializer(serializers.Serializer):
    record_type = serializers.CharField()
    count = serializers.IntegerField()
    latest_date = serializers.DateField()
