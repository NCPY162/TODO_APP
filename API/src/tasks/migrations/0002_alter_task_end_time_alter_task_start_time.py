# Generated by Django 5.1.3 on 2024-11-12 12:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="end_time",
            field=models.TimeField(default=datetime.time(12, 29)),
        ),
        migrations.AlterField(
            model_name="task",
            name="start_time",
            field=models.TimeField(default=datetime.time(12, 29)),
        ),
    ]