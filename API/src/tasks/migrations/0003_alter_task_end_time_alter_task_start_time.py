# Generated by Django 5.1.3 on 2024-11-12 13:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_end_time_alter_task_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end_time',
            field=models.TimeField(default=datetime.time(13, 15)),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.TimeField(default=datetime.time(13, 15)),
        ),
    ]
