# Generated by Django 4.2.1 on 2023-05-08 14:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calendly", "0007_alter_event_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="expired",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name="event",
            name="url",
            field=models.URLField(blank=True, editable=False, null=True),
        ),
    ]