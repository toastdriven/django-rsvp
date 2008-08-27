import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from rsvp.models import Event, Guest
from rsvp.forms import RSVPForm


def event_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    
    if request.POST:
        form = RSVPForm(request.POST)
        
        if form.is_valid():
            guest = form.save()
            return HttpResponseRedirect(reverse('rsvp_event_thanks', kwargs={'slug': slug, 'guest_id': guest.id}))
    else:
        form = RSVPForm()
    
    return render_to_response('rsvp/event_view.html', {
        'event': event,
        'form': form,
    }, context_instance=RequestContext(request))


def event_thanks(request, slug, guest_id):
    event = get_object_or_404(Event, slug=slug)
    
    try:
        guest = event.guests.get(pk=guest_id)
    except Guest.DoesNotExist:
        raise Http404
    
    return render_to_response('rsvp/event_thanks.html', {
        'event': event,
        'guest': guest,
    }, context_instance=RequestContext(request))