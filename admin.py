# pylint: disable=line-too-long

from django.contrib import admin

from .models import ScheduledEvent

@admin.register(ScheduledEvent)
class ScheduledEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'last_seen', 'warning_minutes', 'error_minutes', 'is_warning', 'is_error')
    search_fields = ('event_name',)
    list_filter = ('last_seen',)
