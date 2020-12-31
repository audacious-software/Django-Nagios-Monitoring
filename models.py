# pylint: disable=no-member
# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.utils import timezone

class ScheduledEvent(models.Model):
    event_name = models.CharField(max_length=2048, unique=True)

    last_seen = models.DateTimeField(null=True, blank=True)

    warning_minutes = models.IntegerField(default=5)

    error_minutes = models.IntegerField(default=15)

    def is_warning(self):
        if self.last_seen is None:
            return True

        warning_time = timezone.now() - datetime.timedelta(seconds=(self.warning_minutes * 60))

        return warning_time > self.last_seen

    def is_error(self):
        if self.last_seen is None:
            return True

        error_time = timezone.now() - datetime.timedelta(seconds=(self.error_minutes * 60))

        return error_time > self.last_seen

    @staticmethod
    def log_event(event_name, last_seen, warning_minutes=5, error_minutes=15):
        match = ScheduledEvent.objects.filter(event_name=event_name).first()

        if match is None:
            match = ScheduledEvent(event_name=event_name)
            match.warning_minutes = warning_minutes
            match.error_minutes = error_minutes

        match.last_seen = last_seen

        match.save()
