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
>>> r.context[-1]['event']
<Event: A Test Event>
>>> r.context[-1]['event'].guests_attending()
[<Guest: A Test Event - guest1@example.com - yes>]
>>> r.context[-1]['event'].guests_no_rsvp()
[<Guest: A Test Event - guest2@example.com - no_rsvp>, <Guest: A Test Event - guest3@example.com - no_rsvp>]
>>> type(r.context[-1]['form'])
<class 'rsvp.forms.RSVPForm'>

>>> r = c.post(reverse('rsvp_event_view', args=['a-test-event']), {
...     'email': 'guest99@example.com',
...     'name': 'Guest #99',
...     'attending': 'yes',
...     'number_of_guests': '0',
...     'comment': '',
... })
>>> r.status_code
200
>>> r.context[-1]['form'].errors
{'email': [u'That e-mail is not on the guest list.']}

>>> r = c.post(reverse('rsvp_event_view', args=['a-test-event']), {
...     'email': 'guest1@example.com',
...     'name': 'Guest #1',
...     'attending': 'yes',
...     'number_of_guests': '0',
...     'comment': '',
... })
>>> r.status_code
200
>>> r.context[-1]['form'].errors
{'email': [u'You have already provided RSVP information.']}

>>> r = c.post(reverse('rsvp_event_view', args=['a-test-event']), {
...     'email': 'guest2@example.com',
...     'name': 'Mr. Guest #2',
...     'attending': 'yes',
...     'number_of_guests': '-1',
...     'comment': '',
... })
>>> r.status_code
200
>>> r.context[-1]['form'].errors
{'number_of_guests': [u"The number of guests you're bringing can not be negative."]}

>>> r = c.post(reverse('rsvp_event_view', args=['a-test-event']), {
...     'email': 'guest2@example.com',
...     'name': 'Mr. Guest #2',
...     'attending': 'yes',
...     'number_of_guests': '2',
...     'comment': 'Happy to come and bringing a dish!',
... })
>>> r.status_code
302
>>> r['location']
'http://testserver/rsvp/event/a-test-event/thanks/2/'

>>> r = c.get(reverse('rsvp_event_view', args=['a-test-event']))
>>> r.status_code
200
>>> r.context[-1]['event']
<Event: A Test Event>
>>> r.context[-1]['event'].guests_attending()
[<Guest: A Test Event - guest1@example.com - yes>, <Guest: A Test Event - guest2@example.com - yes>]
>>> r.context[-1]['event'].guests_no_rsvp()
[<Guest: A Test Event - guest3@example.com - no_rsvp>]

>>> r = c.post(reverse('rsvp_event_view', args=['a-test-event']), {
...     'email': 'guest2@example.com',
...     'name': 'Mr. Guest #2',
...     'attending': 'yes',
...     'number_of_guests': '2',
...     'comment': 'Happy to come and bringing a dish!',
... })
>>> r.status_code
200
>>> r.context[-1]['form'].errors
{'email': [u'You have already provided RSVP information.']}
"""
