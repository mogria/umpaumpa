from django.test import Client
from django.test import TestCase
from uuid import uuid4
from .models import Event
import datetime

# Create your tests here.

class PagesTestCase(TestCase):
    fixtures = ['two-events.json']

    def setUp(self):
        self.c = Client()
        self.event = Event.objects.get(pk='88cd5332-235e-4789-8b7d-1eb02c8984bd')

    def testUpcomingEvents(self):
        response = self.c.get('/')
        self.assertTemplateUsed(response, 'punkevents/index.html')
        self.assertContains(response, 'Nächsti Konzis')
        self.assertContains(response, self.event.name)
        self.assertNotContains(response, 'Momentan gids kei nächsti Konzis.')
        assert response.status_code == 200


    def testUpcomingEventsNoEvents(self):
        Event.objects.all().delete()
        response = self.c.get('/')
        self.assertTemplateUsed(response, 'punkevents/index.html')
        self.assertContains(response, 'Nächsti Konzis')
        self.assertNotContains(response, self.event.name)
        self.assertContains(response, 'Momentan gids kei nächsti Konzis.')
        assert response.status_code == 200

    def testSingleEvent(self):
        response = self.c.get('/event/' + str(self.event.id))
        self.assertTemplateUsed(response, 'punkevents/event.html')
        self.assertContains(response, self.event.name)
        self.assertContains(response, self.event.description)
        # self.assertContains(response, self.event.start)
        assert response.status_code == 200

    def testSingleEventNotFound(self):
        response = self.c.get('/event/' + str(uuid4()))
        assert response.status_code == 404
        assert b'Page not found' in response.content
