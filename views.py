import json

import psutil

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

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
            allowed = (ip_address in settings.NAGIOS_MONITOR_ALLOWED_HOSTS)
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
    payload = {
        'cpu_percentage': psutil.cpu_percent(interval=1)
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=201)

@allowed_host
def current_users(request): # pylint: disable=unused-argument
    payload = {
        'count': len(psutil.users())
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=201)

@allowed_host
def disk_usage(request): # pylint: disable=unused-argument
    payload = {}

    partitions = psutil.disk_partitions()

    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)

        payload[partition.device] = usage.percent

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=201)

@allowed_host
def total_processes(request): # pylint: disable=unused-argument
    payload = {
        'count': len(psutil.pids())
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=201)
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

    payload = {
        'count': zombie_count
    }

    return HttpResponse(json.dumps(payload, indent=2), \
                        content_type='application/json', \
                        status=201)
