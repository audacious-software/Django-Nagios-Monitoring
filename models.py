# pylint: disable=no-member, line-too-long
# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.core.checks import Warning, register, registry # pylint: disable=redefined-builtin
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


@register()
def nagios_monitor_deploy_checks(app_configs, **kwargs): # pylint: disable=unused-argument
    errors = []

    deploy_checks = registry.registry.deployment_checks

    for check in deploy_checks:
        check_errors = check(app_configs=app_configs)

        for error in check_errors:
            if (error.id in settings.SILENCED_SYSTEM_CHECKS) is False:
                errors.append(error)

    if len(errors) > 0: # pylint: disable=len-as-condition
        errors.append(Warning('Detected unresolved (or unsilenced) deployment checks.', hint='Address issue or silence checks in SILENCED_SYSTEM_CHECKS.', obj=None, id='nagios_monitor.W001'))

    return errors
