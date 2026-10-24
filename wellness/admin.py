from django.contrib import admin

from .models import WellnessRecord


@admin.register(WellnessRecord)
class WellnessRecordAdmin(admin.ModelAdmin):
    list_display = ['record_type', 'user', 'recorded_date', 'goal', 'created_at']
    list_filter = ['record_type', 'recorded_date']
