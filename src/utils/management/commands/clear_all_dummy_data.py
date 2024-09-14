from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from django.contrib.sessions.models import Session
from django.db import transaction

from finances.models import Invoice

class Command(BaseCommand):
    help = 'Clears all dummy data and resets ID sequences'

    def handle(self, *args, **options):
        self.stdout.write('Starting to clear all data...')
        
        # Handle Session model separately
        self.clear_sessions()

        for model in apps.get_models():
            if model._meta.app_label != 'sessions':  # Skip Session model as we've already handled it
                self.clear_model_data(model)

        self.stdout.write(self.style.SUCCESS('Finished clearing data and resetting sequences'))

    def clear_sessions(self):
        self.stdout.write('Clearing Session data...')
        try:
            Session.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared Session data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing Session data: {str(e)}'))

    def clear_model_data(self, model):
        model_name = model.__name__
        self.stdout.write(f'Clearing data for {model_name}...')
        
        try:
            if model_name == 'CustomUser' or model_name == 'Resident':
            # Find related Invoices and delete them first, FK problem
                Invoice.objects.filter(resident__isnull=False).delete()
            # Use Django's ORM to delete all objects
            model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Cleared data for {model_name}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing {model_name}: {str(e)}'))

        self.reset_sequence(model._meta.db_table)

    def reset_sequence(self, table_name):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), 1, false);")
            self.stdout.write(self.style.SUCCESS(f'Reset ID sequence for {table_name}'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Error resetting sequence for {table_name}: {str(e)}'))