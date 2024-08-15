from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser, Feedback
from finances.models import Invoice, PaidHistory, Card

class Command(BaseCommand):
    help = 'Clears all dummy data from the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('This will delete ALL data from Card, PaidHistory, Invoice, Feedback, and CustomUser models.'))
        self.stdout.write(self.style.WARNING('Are you sure you want to do this?'))
        
        confirm = input(_('Type "yes" to continue, or "no" to cancel: '))
        if confirm.lower() == 'yes':
            self.clear_data()
        else:
            self.stdout.write(self.style.SUCCESS('Operation cancelled.'))

    def clear_data(self):
        # Clear Card data
        card_count = Card.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Deleted {card_count} Card records'))

        # Clear PaidHistory data
        paid_history_count = PaidHistory.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Deleted {paid_history_count} PaidHistory records'))

        # Clear Invoice data
        invoice_count = Invoice.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Deleted {invoice_count} Invoice records'))

        # Clear Feedback data
        feedback_count = Feedback.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Deleted {feedback_count} Feedback records'))

        # Clear CustomUser data (which includes Resident data)
        user_count = CustomUser.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Deleted {user_count} CustomUser records'))

        self.stdout.write(self.style.SUCCESS('All dummy data has been cleared from the database'))