from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns(
    '',
    host(r'', 'jtcalumn.urls', name = 'index'),
)