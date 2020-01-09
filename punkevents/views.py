from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.utils.translation import gettext as _
from .models import Event

# Create your views here.
def upcoming(request):
    return render(request, 'punkevents/index.html', {
        'events': Event.objects.order_by('start')[:10]
    })


def event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        return render(request, 'punkevents/event.html', {
            'event': event
        })
    except Event.DoesNotExist:
        raise Http404(_("Event with UUID %(uuid) was not found.") % {
            'uuid': event_id,
        })

def date(request, date):
    try:
        events = Event.objects.get(start=date)
    except Event.DoesNotExist:
        events = []
    return render(request, 'punkevents/date.html', {
        'events': events
    })


def venue(request, venue_id):
    return render(request, 'punkevents/venue.html', {
        'venue': None
    })

def page_not_found(request, *args, **kwargs):
    response = render(request, 'punkevents/404.html', {})
    response.status_code = 404
    return response
