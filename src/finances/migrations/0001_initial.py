# Generated by Django 5.1 on 2024-09-18 14:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_no', models.CharField(max_length=20, unique=True)),
                ('card_type', models.CharField(choices=[('visa', 'Visa'), ('mastercard', 'Mastercard'), ('amex', 'Amex')], max_length=20)),
                ('card_expiry', models.DateField()),
                ('card_cvv', models.CharField(max_length=4)),
                ('card_name', models.CharField(max_length=100)),
                ('card_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=20)),
                ('card_created_at', models.DateTimeField(auto_now_add=True)),
                ('card_updated_at', models.DateTimeField(auto_now=True)),
                ('card_deleted_at', models.DateTimeField(blank=True, null=True)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='card', to='users.resident')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=20, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], max_length=20)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices', to='users.resident')),
            ],
        ),
        migrations.CreateModel(
            name='PaidHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_at', models.DateTimeField(auto_now_add=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paid_history', to='finances.invoice')),
            ],
        ),
    ]
