# Generated by Django 4.2.1 on 2023-05-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calendly", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
