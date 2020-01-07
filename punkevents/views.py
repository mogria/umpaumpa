from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
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
        raise Http404("Event with UUID " + str(event_id) + " was not found.")

def date(request, date):
    pass


def venue(request, date):
    pass

def page_not_found(request, *args, **kwargs):
    response = render(request, 'punkevents/404.html', {})
    response.status_code = 404
    return response
