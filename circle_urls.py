import sys

import django

if sys.version_info[0] > 2:
    from django.urls import re_path as url
else:
    from django.conf.urls import url

urlpatterns = [
    url(r'^admin/', django.contrib.admin.site.urls),
    url(r'^monitor/', include('nagios_monitor.urls')),
]
