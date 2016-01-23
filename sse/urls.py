from django.conf.urls import patterns, include, url

from views import home, sse

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^sse/$', sse, name='home'),
)
