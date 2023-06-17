import hashlib

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Event(models.Model):
    user_created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=50, blank=False)
    start_time = models.DateTimeField("Start time", blank=False)
    end_time = models.DateTimeField("End time", blank=False)
    expired = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    max_amount_of_joiners = models.PositiveSmallIntegerField(default=1)
    hash_url = models.URLField(default=None, editable=False, unique=True)

    def __str__(self):
        return f"{self.name} {self.user_created}"

    def get_hashed_url(self):
        # Change if better solution then event name and user created name combo
        identifier = str(self.name) + str(self.user_created)
        hash_obj = hashlib.md5(identifier.encode())
        return hash_obj.hexdigest()

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("calendly:event_detail", args=(self.hash_url,))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.hash_url = self.get_hashed_url()
        super().save(*args, **kwargs)


class EventJoinUser(models.Model):
    full_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name} {self.email}"

    def clean(self):
        super().clean()
        existing_joiners = self.event.eventjoinuser_set.count()
        if existing_joiners >= self.event.max_amount_of_joiners:
            if self.pk:  # If the instance is being updated
                # Exclude the current instance from the count
                existing_joiners -= 1
            if existing_joiners >= self.event.max_amount_of_joiners:
                raise ValidationError("Maximum number of joiners exceeded for this event.")
