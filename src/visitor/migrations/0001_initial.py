# Generated by Django 5.0.7 on 2024-08-02 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('hp_number', models.CharField(max_length=100)),
                ('car_place_no', models.CharField(max_length=100)),
                ('check_in_date', models.DateTimeField()),
                ('check_out_date', models.DateTimeField(null=True)),
                ('check_in_time', models.DateTimeField()),
                ('check_out_time', models.DateTimeField(null=True)),
                ('purpose_of_visit', models.CharField(max_length=100)),
                ('parking_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='visitor_id', to='parking.visitorparking')),
            ],
        ),
    ]
