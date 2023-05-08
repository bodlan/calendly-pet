# Generated by Django 4.2.1 on 2023-05-08 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calendly", "0003_event_url_user_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="expired",
            field=models.BooleanField(editable=False),
        ),
        migrations.AlterField(
            model_name="event",
            name="url",
            field=models.URLField(editable=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=255),
        ),
    ]
