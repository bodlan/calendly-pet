# Generated by Django 4.2.1 on 2023-05-08 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calendly", "0006_alter_event_expired_alter_event_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
