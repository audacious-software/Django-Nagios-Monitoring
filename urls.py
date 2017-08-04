# pylint: disable=line-too-long

from django.conf.urls import url

from .views import cpu_load, current_users, disk_usage, total_processes, zombie_processes

urlpatterns = [
    url(r'^cpu-load.json$', cpu_load, name='nagios_monitor_cpu_load'),
    url(r'^current-users.json$', current_users, name='nagios_monitor_current_users'),
    url(r'^disk-usage.json$', disk_usage, name='nagios_monitor_disk_usage'),
    url(r'^total-processes.json$', total_processes, name='nagios_monitor_total_processes'),
    url(r'^zombie-processes.json$', zombie_processes, name='nagios_monitor_zombie_processes'),
]
