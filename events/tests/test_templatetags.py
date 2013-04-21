from django.test import TestCase
from django.template import Template, RequestContext
from events.models import Event, Calendar
from events.templatetags.events import querystring_for_date
from events.periods import Day
import datetime


class TestTemplateTags(TestCase):
    fixtures = ['events.json']

    def test_querystring_for_datetime(self):
        date = datetime.datetime(2008, 1, 1, 0, 0, 0)
        query_string = querystring_for_date(date)
        self.assertEqual("?year=2008&month=1&day=1&hour=0&minute=0&second=0", query_string)

    def test_all_day_events_list(self):

        # get a response object in order to use the request data for testing
        request = self.client.get("/").context['request']

        # test the tag with no all day events
        day = Day(Event.objects.all())
        c = RequestContext(request, {'day': day})
        out = Template('{% load events %}{% all_day_events_list day %}').render(c)
        self.assertEqual(out.strip(), "")

        # test the tag with one all day event
        start = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)
        end = datetime.datetime.combine(datetime.datetime.now(), datetime.time.max)
        cal = Calendar.objects.all().get()
        Event.objects.create(start=start, end=end, all_day=True, title="Test All Day Event", calendar=cal)
        day = Day(Event.objects.all())
        c = RequestContext(request, {'day': day})
        out = Template('{% load events %}{% all_day_events_list day %}').render(c)
        self.assertTrue('Test All Day Event' in out)
