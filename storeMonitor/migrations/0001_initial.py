# Generated by Django 4.2.3 on 2023-09-22 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusinessHours",
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
                ("store_id", models.CharField(max_length=255)),
                ("day_of_week", models.PositiveIntegerField()),
                ("start_time_local", models.TimeField()),
                ("end_time_local", models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name="PollData",
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
                ("store_id", models.CharField(max_length=255)),
                ("timestamp_utc", models.DateTimeField()),
                ("status", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Timezone",
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
                ("store_id", models.CharField(max_length=255)),
                (
                    "timezone_str",
                    models.CharField(default="America/Chicago", max_length=255),
                ),
            ],
        ),
    ]