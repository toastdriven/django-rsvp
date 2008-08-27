"""
>>> from django.core.management import call_command
>>> call_command('loaddata', 'rsvp_testdata.yaml') #doctest: +ELLIPSIS
Installing yaml fixture 'rsvp_testdata' ...
Installed 4 object(s) from 1 fixture(s)

>>> from django.test import Client
>>> c = Client()

>>> from django.core import mail
>>> from django.core.urlresolvers import reverse
>>> from rsvp.models import Event, Guest

>>> r = c.get(reverse('rsvp_event_view', args=['a-test-event']))
>>> r.status_code
200
"""
