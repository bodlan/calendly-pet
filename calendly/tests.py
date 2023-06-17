from django.urls import reverse
from django.test import TestCase
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Event


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.users = get_user_model().objects.all()

    def test_user_creation(self):
        self.assertTrue(self.user.username == "testuser")
        self.assertIsNotNone(self.users.filter(username=self.user.username))

    def test_user_password_change(self):
        self.user.password = "newpassword"
        self.user.save()
        self.assertTrue("newpassword", self.user.password)

    def test_user_deletion(self):
        self.user.delete()
        self.assertQuerySetEqual(self.users.filter(username=self.user.username), [])

    def test_user_events(self):
        test_event = Event.objects.create(
            user_created=self.user,
            name="test Event",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=12),
        )
        self.assertEqual(test_event.user_created, self.user)
        self.user.delete()
        self.assertQuerySetEqual(Event.objects.filter(user_created=self.user), [])


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.event = Event.objects.create(
            user_created=self.user,
            name="Test Event",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
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
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            hidden=True,
        )
        self.event2 = Event.objects.create(
            user_created=self.user,
            name="Test Event2",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
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
