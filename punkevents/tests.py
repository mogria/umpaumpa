from django.utils.translation import ugettext as _
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
        self.assertContains(response, _('Upcoming Events'))
        self.assertNotContains(response, self.event.name)
        self.assertContains(response, 'Momentan gids kei nächsti Konzis.')
        assert response.status_code == 200

    def testUpcomingEventsNoCalendarEvents(self):
        Event.objects.all().delete()
        response = self.c.get('/')
        self.assertTemplateUsed(response, 'punkevents/index.html')
        self.assertContains(response, _('Calendar'))
        self.assertContains(response, _("Currently there are no event dates available in the calendar"))
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
        assert _('Page not found') in response.content.decode('utf-8')


    def testByDate(self):
        test_date = datetime.date(2019, 1, 5)
        response = self.c.get('/date/' + test_date.isoformat())
        test_date.isocalendar
        self.assertContains(response, '2019')
        self.assertContains(response, '5')

    def testByDateNoEvents(self):
        test_date = datetime.date(2019, 1, 1)
        response = self.c.get('/date/' + test_date.isoformat())
        self.assertContains(response, _('No event at this date'))
