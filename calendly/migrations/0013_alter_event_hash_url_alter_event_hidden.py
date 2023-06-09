# Generated by Django 4.2.1 on 2023-05-12 17:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calendly", "0012_alter_event_expired"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="hash_url",
            field=models.URLField(default=None, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="hidden",
            field=models.BooleanField(default=False),
        ),
    ]
