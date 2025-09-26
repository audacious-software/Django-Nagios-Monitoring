# pylint: disable=no-member, line-too-long

import datetime
import importlib
import json
import os

import boto3
import psutil

from botocore.config import Config

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils import timezone

from .models import ScheduledEvent

def allowed_host(function):
    def wrap(request, *args, **kwargs):
        ip_address = None

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        allowed = True

        try:
            allowed = (ip_address in settings.NAGIOS_MONITOR_ALLOWED_HOSTS) # pylint: disable=superfluous-parens
        except AttributeError:
            pass

        if allowed:
            return function(request, *args, **kwargs)

        raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap

@allowed_host
def cpu_load(request): # pylint: disable=unused-argument
    cpu_percentage = psutil.cpu_percent(interval=1)

    payload = {
        'cpu_percentage': cpu_percentage,
        'cpu_status': 'normal',
    }

    critical = 95

    if hasattr(settings, 'NAGIOS_MONITOR_CPU_CRITICAL'):
        critical = settings.NAGIOS_MONITOR_CPU_CRITICAL

    warning = 80

    if hasattr(settings, 'NAGIOS_MONITOR_CPU_WARNING'):
        warning = settings.NAGIOS_MONITOR_CPU_WARNING

    if cpu_percentage >= critical:
        payload['cpu_status'] = 'critical'
    elif cpu_percentage >= warning:
        payload['cpu_status'] = 'warning'

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=200)

@allowed_host
def current_users(request): # pylint: disable=unused-argument
    payload = {
        'count': len(psutil.users())
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=200)

@allowed_host
def disk_usage(request): # pylint: disable=unused-argument
    payload = {}

    partitions = psutil.disk_partitions()

    for partition in partitions:
        if ('/dev/loop' in partition.device) is False:
            try:
                usage = psutil.disk_usage(partition.mountpoint)

                if hasattr(settings, 'NAGIOS_MONITOR_IGNORE_DISKS') and partition.device in settings.NAGIOS_MONITOR_IGNORE_DISKS:
                    pass
                else:
                    payload[partition.device] = usage.percent
            except OSError:
                pass

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=200)

@allowed_host
def total_processes(request): # pylint: disable=unused-argument
    payload = {
        'count': len(psutil.pids())
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=200)
@allowed_host
def zombie_processes(request): # pylint: disable=unused-argument
    zombie_count = 0

    for pid in psutil.pids():
        try:
            process = psutil.Process(pid=pid)

            if process.status() == psutil.STATUS_ZOMBIE:
                zombie_count += 1
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass

    payload = {
        'count': zombie_count
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=200)


@allowed_host
def background_jobs(request): # pylint: disable=unused-argument
    warnings = []
    errors = []

    for event in ScheduledEvent.objects.all():
        if event.is_error():
            errors.append(event.event_name)
        elif event.is_warning():
            warnings.append(event.event_name)

    payload = {
        'errors': errors,
        'warnings': warnings,
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=200)

@allowed_host
def other_issues(request): # pylint: disable=unused-argument
    issues = []

    for app in settings.INSTALLED_APPS:
        try:
            monitor_module = importlib.import_module('.monitoring_api', package=app)

            for issue in monitor_module.issues():
                issues.append(('%s: %s' % (app, issue)))
        except ImportError:
            pass
        except AttributeError:
            pass


    payload = {
        'issues': issues,
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=200)

# @allowed_host
def aws_ec2_remaining_credits(request, instance_id, region_id=None): # pylint: disable=unused-argument, too-many-locals
    proceed = True

    warnings = []

    if hasattr(settings, 'MONITOR_AWS_REGION') is False:
        warnings.append('Missing MONITOR_AWS_REGION settings parameter.')

        proceed = False

    if hasattr(settings, 'MONITOR_AWS_ACCESS_KEY_ID') is False:
        warnings.append('Missing MONITOR_AWS_ACCESS_KEY_ID settings parameter.')

        proceed = False

    if hasattr(settings, 'MONITOR_AWS_SECRET_ACCESS_KEY') is False:
        warnings.append('Missing MONITOR_AWS_SECRET_ACCESS_KEY settings parameter.')

        proceed = False

    payload = {
        'credits_remaining': 0,
        'warnings': warnings
    }

    if proceed:
        end = timezone.now()
        start = end - datetime.timedelta(days=7)

        if region_id is None:
            region_id = settings.MONITOR_AWS_REGION

        aws_config = Config(
            region_name=region_id,
            retries={'max_attempts': 10, 'mode': 'standard'}
        )

        os.environ['AWS_ACCESS_KEY_ID'] = settings.MONITOR_AWS_ACCESS_KEY_ID
        os.environ['AWS_SECRET_ACCESS_KEY'] = settings.MONITOR_AWS_SECRET_ACCESS_KEY

        client = boto3.client('cloudwatch', config=aws_config)

        response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUCreditBalance',
            Dimensions=[{
                'Name': 'InstanceId',
                'Value': instance_id
                },],
            StartTime=start,
            EndTime=end,
            Period=3600,
            Statistics=[
                'Minimum',
                'Maximum',
                'Average',
            ],
            Unit='Count'
        )

        largest_maximum = 0
        latest_average = 0
        latest_recording = None

        for datapoint in response.get('Datapoints', []):
            if latest_recording is None:
                latest_recording = datapoint.get('Timestamp', None)

            when = datapoint.get('Timestamp', None)
            average = datapoint.get('Average', 0)
            maximum = datapoint.get('Maximum', 0)

            if when > latest_recording:
                latest_recording = when

                latest_average = average

            largest_maximum = max(largest_maximum, maximum)

        if largest_maximum > 0:
            payload['credits_remaining'] = latest_average / largest_maximum

        payload['latest_balance'] = latest_average
        payload['maximum_observed'] = largest_maximum

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=200)
