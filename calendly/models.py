import hashlib

import pytz
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, unique=True, blank=False)
    password = models.CharField(max_length=255, blank=False)
    join_date = models.DateField(auto_now_add=True)
    timezone = models.CharField(max_length=50, default="UTC")

    def __str__(self):
        return f"{self.username} {self.join_date}"

    def save(self, *args, **kwargs):
        if self.pk:
            user = User.objects.get(pk=self.pk)
        if not self.pk or self.password != user.password:
            self.password = make_password(self.password)
        elif self.timezone != user.timezone:
            user_events = user.event_set.all()
            for user_event in user_events:
                user_event.save()
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Event(models.Model):
    user_created = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    start_time = models.DateTimeField("Start time")
    end_time = models.DateTimeField("End time")
    expired = models.BooleanField(default=False, editable=False)
    hidden = models.BooleanField()
    hash_url = models.URLField(blank=True, null=True, editable=False, unique=True)

    def __str__(self):
        return f"{self.name} {self.user_created}"

    def get_hashed_url(self):
        identifier = self.name + str(self.user_created)
        hash_obj = hashlib.md5(identifier.encode())
        return hash_obj.hexdigest()

    def time_in_user_timezone(self, time):
        """
        Returns the time of the event in the user's timezone.
        """
        timezone_obj = pytz.timezone(self.user_created.timezone)
        # TODO: change this workaround of timezones in future
        try:
            return timezone_obj.localize(time)
        except ValueError:
            return time

    def save(self, *args, **kwargs):
        # TODO: change start_time and end_time handle with timezone change in User model
        if not self.pk:
            self.hash_url = self.get_hashed_url()
            self.start_time = self.time_in_user_timezone(self.start_time)
            self.end_time = self.time_in_user_timezone(self.end_time)

        super().save(*args, **kwargs)
