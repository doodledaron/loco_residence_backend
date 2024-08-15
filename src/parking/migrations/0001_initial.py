# Generated by Django 5.0.7 on 2024-08-02 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('residence', '0001_initial'),
        ('users', '0003_alter_customuser_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parking_created_at', models.DateTimeField(auto_now_add=True)),
                ('parking_updated_at', models.DateTimeField(auto_now=True)),
                ('parking_deleted_at', models.DateTimeField(blank=True, null=True)),
                ('block_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parkings', to='residence.block')),
            ],
        ),
        migrations.CreateModel(
            name='ResidentParking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_no', models.CharField(max_length=100)),
                ('is_occupied', models.BooleanField(default=False)),
                ('parking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident_parkings', to='parking.parking')),
                ('resident_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident_parkings', to='users.resident')),
            ],
        ),
        migrations.CreateModel(
            name='VisitorParking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_no', models.CharField(max_length=100)),
                ('is_occupied', models.BooleanField(default=False)),
                ('parking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking', to='parking.parking')),
            ],
        ),
    ]