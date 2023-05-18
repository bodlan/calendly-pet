from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Event


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")

    def test_user_creation(self):
        self.assertTrue(check_password("testpassword", self.user.password))
        self.assertTrue(self.user.join_date == datetime.today().date())

    def test_user_password_change(self):
        self.user.password = "newpassword"
        self.user.save()
        self.assertTrue(check_password("newpassword", self.user.password))


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.event = Event.objects.create(
            user_created=self.user,
            name="Test Event",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            hidden=False,
        )

    def test_event_creation(self):
        self.assertFalse(self.event.expired)
        self.assertFalse(self.event.hidden)
        self.assertTrue(self.event.hash_url)

    def test_event_hash_url(self):
        self.assertEqual(self.event.hash_url, Event.get_hashed_url(self.event))


class EventIndexViewTests(TestCase):
    def user_event_creation(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.event = Event.objects.create(
            user_created=self.user,
            name="Test Event",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            hidden=True,
        )
        self.event2 = Event.objects.create(
            user_created=self.user,
            name="Test Event2",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            hidden=True,
        )

    def test_no_events(self):
        """
        If no current events message displayed
        """
        response = self.client.get(reverse("calendly:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No events are available.")
        self.assertQuerySetEqual(response.context["events"], [])

    def test_events_not_showing(self):
        self.user_event_creation()
        self.test_no_events()

    def test_event_visible(self):
        self.user_event_creation()
        self.event.hidden = False
        self.event.save()
        response = self.client.get(reverse("calendly:index"))
        self.assertQuerySetEqual(response.context["events"], [self.event])
