# Generated by Django 4.2.1 on 2023-05-08 13:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calendly", "0002_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="url",
            field=models.URLField(default="default"),
        ),
        migrations.AddField(
            model_name="user",
            name="password",
            field=models.CharField(default="default", max_length=255),
        ),
    ]