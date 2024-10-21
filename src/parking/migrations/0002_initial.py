# Generated by Django 5.1 on 2024-09-18 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parking', '0001_initial'),
        ('visitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorparking',
            name='visitor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='visitors_parkings', to='visitor.visitor'),
        ),
        migrations.AddIndex(
            model_name='parking',
            index=models.Index(fields=['parking_no'], name='parking_par_parking_bd66bb_idx'),
        ),
    ]