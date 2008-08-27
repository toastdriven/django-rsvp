from django.conf.urls.defaults import *


urlpatterns = patterns('rsvp.views',
    url(r'^event/(?P<slug>[A-Za-z0-9_-]+)/$', 'event_view', name='rsvp_event_view'),
    url(r'^event/(?P<slug>[A-Za-z0-9_-]+)/thanks/(?P<guest_id>\d+)/$', 'event_thanks', name='rsvp_event_thanks'),
)
