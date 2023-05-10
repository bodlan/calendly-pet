from django.test import TestCase
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from .models import User, Event


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
