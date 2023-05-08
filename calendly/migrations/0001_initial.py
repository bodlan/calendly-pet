# Generated by Django 4.2.1 on 2023-05-08 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=20)),
                ("join_date", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("start_time", models.DateTimeField(verbose_name="Start time")),
                ("end_time", models.DateTimeField(verbose_name="End time")),
                ("expired", models.BooleanField()),
                ("hidden", models.BooleanField()),
                (
                    "user_created",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="calendly.user"),
                ),
            ],
        ),
    ]
