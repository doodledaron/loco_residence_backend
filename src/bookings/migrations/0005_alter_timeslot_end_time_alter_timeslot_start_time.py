# Generated by Django 5.1 on 2024-10-21 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_alter_timeslot_end_time_alter_timeslot_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2024, 10, 21, 23, 53, 50, 82102)),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2024, 10, 21, 23, 53, 50, 82102)),
        ),
    ]
