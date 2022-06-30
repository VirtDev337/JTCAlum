from django_hosts import patterns, host
from django.conf import settings

prefix = '.static.projects.'

host_patterns = patterns(
    '',
    host(r'', settings.ROOT_URLCONF, name = 'index'),
    host(r'www', settings.ROOT_URLCONF, name = 'web-index'),
    
    host(r'<str:owner>/<str:slug>/demo', prefix.join('<str:title>.<str:site>.urls.py'), name = 'demo' ),
)