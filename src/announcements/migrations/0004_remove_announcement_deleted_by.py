# Generated by Django 5.1 on 2024-09-15 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0003_remove_announcement_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='deleted_by',
        ),
    ]
