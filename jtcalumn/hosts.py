from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'jtcalumn.urls', name='index'),
)