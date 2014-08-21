===============================
django-rsvp: A simple RSVP app.
===============================

``django-rsvp`` is a simple RSVP application for use with Django. The intent
is to be able to basic events, send guests invite e-mails and collect their
response if they will be attending or not.


Requirements
============

``django-rsvp`` requires:

* Python 2.3+
* Django 1.0+

The only potential dependency within Django is that ``django.contrib.sites``
is in ``INSTALLED_APPS`` in order to make the included e-mail template work.


Installation
============

#. Either copy/symlink the ``rsvp`` app into your project or place it
   somewhere on your ``PYTHONPATH``.
#. Add ``rvsp`` app to your ``INSTALLED_APPS``.
#. Set the ``RSVP_FROM_EMAIL`` setting to an e-mail address you'd like
   invites to be sent from.
#. Run ``./manage.py syncdb``.
#. Add ``(r'^rsvp/', include('rsvp.urls')),`` to your
   ``urls.py``.
