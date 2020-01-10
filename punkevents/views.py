from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.utils.translation import gettext as _
from django.utils.timezone import make_aware

from .models import Event
import datetime

# Create your views here.
def upcoming(request):
    return render(request, 'punkevents/index.html', {
        'events': Event.objects.order_by('start')[:10],
        'calendar_events': False, # Event.objects('start')
    })


def event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        return render(request, 'punkevents/event.html', {
            'event': event
        })
    except Event.DoesNotExist:
        raise Http404(_("Event with UUID %(uuid)s was not found.") % {
            'uuid': str(event_id),
        })

def date(request, date):
    parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d" )
    date = make_aware(parsed_date)
    try:
        events = Event.objects.get(start=date)
        print(events)
    except Event.DoesNotExist:
        events = []
    return render(request, 'punkevents/date.html', {
        'events': events,
        'date': parsed_date
    })


def venue(request, venue_id):
    return render(request, 'punkevents/venue.html', {
        'venue': None
    })

def page_not_found(request, *args, **kwargs):
    return render(request, 'punkevents/404.html', status=404)
