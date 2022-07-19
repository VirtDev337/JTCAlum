from django_hosts import patterns, host
from django.conf import settings

prefix = 'demos.'

host_patterns = patterns(
    '',
    host(r'', settings.ROOT_URLCONF, name = 'index'),
    host(r'www', settings.ROOT_URLCONF, name = 'web-index'),
    
    host(r'http[s]?://jtcalum.org/<str:slug>/', prefix.join('<str:user>.<str:title>.<str:site>.urls'), name = 'demo' ),
)
