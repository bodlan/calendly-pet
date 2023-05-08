from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} {self.join_date}"


class Event(models.Model):
    user_created = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField("Start time")
    end_time = models.DateTimeField("End time")
    expired = models.BooleanField()
    hidden = models.BooleanField()

    def __str__(self):
        return f"{self.name} {self.user_created}"
