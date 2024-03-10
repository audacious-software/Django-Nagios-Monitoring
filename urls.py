# pylint: disable=line-too-long, wrong-import-position

import sys

if sys.version_info[0] > 2:
    from django.urls import re_path as url # pylint: disable=no-name-in-module
else:
    from django.conf.urls import url

from .views import cpu_load, current_users, disk_usage, total_processes, zombie_processes, \
                   background_jobs, other_issues, aws_ec2_remaining_credits

urlpatterns = [
    url(r'^cpu-load.json$', cpu_load, name='nagios_monitor_cpu_load'),
    url(r'^current-users.json$', current_users, name='nagios_monitor_current_users'),
    url(r'^disk-usage.json$', disk_usage, name='nagios_monitor_disk_usage'),
    url(r'^total-processes.json$', total_processes, name='nagios_monitor_total_processes'),
    url(r'^zombie-processes.json$', zombie_processes, name='nagios_monitor_zombie_processes'),
    url(r'^background-jobs.json$', background_jobs, name='nagios_monitor_background_jobs'),
    url(r'^other-issues.json$', other_issues, name='nagios_monitor_other_issues'),
    url(r'^ec2/(?P<region_id>.+)/(?P<instance_id>.+)/remaining-credits.json$', aws_ec2_remaining_credits, name='aws_ec2_remaining_credits_region'),
    url(r'^ec2/(?P<instance_id>.+)/remaining-credits.json$', aws_ec2_remaining_credits, name='aws_ec2_remaining_credits'),
]
