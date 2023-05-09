import hashlib

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, unique=True, blank=False)
    password = models.CharField(max_length=255, blank=False)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} {self.join_date}"

    def save(self, *args, **kwargs):
        if not self.pk or self.password != User.objects.get(pk=self.pk).password:
            self.password = make_password(self.password)
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
    url = models.URLField(blank=True, null=True, editable=False, unique=True)

    def __str__(self):
        return f"{self.name} {self.user_created}"

    def get_hashed_url(self):
        identifier = self.name + str(self.start_time) + str(self.end_time)
        hash_obj = hashlib.md5(identifier.encode())
        return hash_obj.hexdigest()

    def get_absolute_url(self):
        return reverse("calendly:event_detail", args=[self.get_hashed_url()])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.url = self.get_absolute_url()
        super().save(*args, **kwargs)
