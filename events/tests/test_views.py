from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import Client
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from events.views import check_next_url, coerce_date_dict
from events.models import Event, Occurrence
import datetime
import time


class TestViewUtils(TestCase):

    def test_check_next_url(self):
        url = "http://thauber.com"
        self.assertTrue(check_next_url(url) is None)
        url = "/hello/world/"
        self.assertEqual(url, check_next_url(url))

    def test_coerce_date_dict(self):
        self.assertEqual(
            coerce_date_dict({'year': '2008', 'month': '4', 'day': '2', 'hour': '4', 'minute': '4', 'second': '4'}),
            {'year': 2008, 'month': 4, 'day': 2, 'hour': 4, 'minute': 4, 'second': 4}
            )

    def test_coerce_date_dict_partial(self):
        self.assertEqual(
            coerce_date_dict({'year': '2008', 'month': '4', 'day': '2'}),
            {'year': 2008, 'month': 4, 'day': 2, 'hour': 0, 'minute': 0, 'second': 0}
            )

    def test_coerce_date_dict_empty(self):
        self.assertEqual(
            coerce_date_dict({}),
            {}
            )

    def test_coerce_date_dict_missing_values(self):
        self.assertEqual(
            coerce_date_dict({'year': '2008', 'month': '4', 'hours': '3'}),
            {'year': 2008, 'month': 4, 'day': 1, 'hour': 0, 'minute': 0, 'second': 0}
            )


c = Client()


class TestUrls(TestCase):

    fixtures = ['events.json']
    highest_event_id = 7

    def test_calendar_view(self):
        self.response = c.get(
            reverse("year_calendar", kwargs={"calendar_slug": 'example'}), {})
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context[0]["calendar"].name,
                         "Example Calendar")

    def test_calendar_month_view(self):
        self.response = c.get(reverse("month_calendar", kwargs={"calendar_slug": 'example'}), {'year': 2000, 'month': 11})
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context[0]["calendar"].name, "Example Calendar")
        month = self.response.context[0]["periods"]['month']
        self.assertEqual((month.start, month.end), (datetime.datetime(2000, 11, 1, 0, 0), datetime.datetime(2000, 12, 1, 0, 0)))

    def test_event_creation_anonymous_user(self):
        self.response = c.get(reverse("calendar_create_event",
                                      kwargs={"calendar_slug": 'example'}),
                              {})
        self.assertEqual(self.response.status_code, 302)

    def test_event_creation_authenticated_user(self):
        c.login(username="admin", password="admin")
        self.response = c.get(reverse("calendar_create_event",
                                      kwargs={"calendar_slug": 'example'}),
                              {})
        self.assertEqual(self.response.status_code, 200)

        self.response = c.post(reverse("calendar_create_event",
                                      kwargs={"calendar_slug": 'example'}),
                               {'description': 'description',
                                'title': 'title',
                                'end_recurring_period_1': '10:22:00', 'end_recurring_period_0': '2008-10-30', 'end_recurring_period_2': 'AM',
                                'end_1': '10:22:00', 'end_0': '2008-10-30', 'end_2': 'AM',
                                'start_0': '2008-10-30', 'start_1': '09:21:57', 'start_2': 'AM'
                               })
        self.assertEqual(self.response.status_code, 302)

        highest_event_id = self.highest_event_id
        highest_event_id += 1
        self.response = c.get(reverse("event",
                                      kwargs={"event_id": highest_event_id}), {})
        self.assertEqual(self.response.status_code, 200)
        c.logout()

    def test_view_event(self):
        self.response = c.get(reverse("event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 200)

    def test_delete_event_anonymous_user(self):
        # Only logged-in users should be able to delete, so we're redirected
        self.response = c.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 302)

    def test_delete_event_authenticated_user(self):
        c.login(username="admin", password="admin")

        # Load the deletion page
        self.response = c.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 200)

        # Delete the event
        self.response = c.post(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 302)

        # Since the event is now deleted, we get a 404
        self.response = c.get(reverse("delete_event", kwargs={"event_id": 1}), {})
        self.assertEqual(self.response.status_code, 404)
        c.logout()

    def test_adding_events(self):
        c.login(username="admin", password="admin")

        # test adding an all day weekly repeating event
        old_count = Event.objects.all().count()
        now = datetime.datetime.now()
        now_date_str = now.strftime('%Y-%m-%d')
        self.response = c.post(reverse("calendar_create_event", args=['example']), {
            'start_0': now_date_str,
            'start_1': '',
            'end_0': now_date_str,
            'end_1': '',
            'all_day': 'Checked',
            'title': 'Test All Day Event',
            'rule': 3,
        })
        self.assertTrue(old_count < Event.objects.all().count())
        self.assertEqual(self.response.status_code, 302)

        # test adding an persistent occurrence
        old_occ_count = Occurrence.objects.all().count()
        all_day_event = Event.objects.filter(title="Test All Day Event").get()
        occurrences = all_day_event.get_occurrences(all_day_event.start + datetime.timedelta(weeks=2), all_day_event.start + datetime.timedelta(weeks=10))
        occ = occurrences[0]
        occ_date_str = occ.start.strftime('%Y-%m-%d')
        post_data = {
            'title': "Test All Day Event (Single Persisted)",
            'start_0': occ_date_str,
            'start_1': '9:00:00',
            'end_0': occ_date_str,
            'end_1': '10:00:00',
        }
        self.response = c.post(reverse('edit_occurrence_by_date', kwargs={
                'event_id': occ.event.id,
                'year': occ.start.year,
                'month': occ.start.month,
                'day': occ.start.day,
                'hour': occ.start.hour,
                'minute': occ.start.minute,
                'second': occ.start.second,
            }), post_data)
        self.assertEqual(self.response.status_code, 302)
        self.assertTrue(old_occ_count < Occurrence.objects.all().count())


class MySeleniumTests(LiveServerTestCase):
    """
    In order to run tests you'll need to download and install the Selenium
    Chrome driver from http://code.google.com/p/selenium/downloads/list. Just
    download and extra that driver and make sure it's in your path. I put mine
    in /usr/localbin.
    """

    fixtures = ['events.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_invalid_login(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('foo')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('foo')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # Wait until the response is received
        WebDriverWait(self.selenium, 2).until(lambda driver: driver.find_element_by_tag_name('body'))
        self.assertTrue(self.selenium.find_element_by_xpath('//div[contains(@class, "alert-error")]/strong').text.startswith("Your username and password didn't match. Please try again."))

    def test_valid_login(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # Wait until the response is received
        WebDriverWait(self.selenium, 2).until(lambda driver: driver.find_element_by_tag_name('body'))
        self.assertTrue(self.selenium.find_element_by_xpath('//div[@class="container"]/div[@class="hero-unit"]/p').text.startswith("Welcome to Django-schedule's"))

    def test_creating_all_day_event(self):

        # login first
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # Wait until the response is received
        WebDriverWait(self.selenium, 2).until(lambda driver: driver.find_element_by_tag_name('body'))

        self.selenium.get('%s%s' % (self.live_server_url, reverse("calendar_create_event", kwargs={"calendar_slug": 'example'})))
        self.selenium.find_element_by_id('id_start_0').click()
        self.selenium.find_element_by_xpath('//td[contains(@class, "ui-datepicker-today")]/a').click()
        time.sleep(0.1)
        self.selenium.find_element_by_id('id_end_0').click()
        self.selenium.find_element_by_xpath('//td[contains(@class, "ui-datepicker-today")]/a').click()
        time.sleep(0.1)
        self.selenium.find_element_by_id('id_all_day').click()
        username_input = self.selenium.find_element_by_name("title")
        username_input.send_keys('Example All Day Event')

        # self.selenium.find_element_by_id('id_rule').click()
        self.selenium.find_element_by_xpath('//select[@name="rule"]/option[3]').click()
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # Wait until the response is received
        WebDriverWait(self.selenium, 2).until(lambda driver: driver.find_element_by_tag_name('body'))
        self.assertEqual(self.selenium.find_element_by_xpath('//div[@id="event-detail-wrap"]//div[@class="period-name"]/strong').text, 'Example All Day Event')
