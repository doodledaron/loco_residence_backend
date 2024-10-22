# file: management/commands/generate_dummy_data.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from users.models import Resident, Feedback
from finances.models import Invoice, PaidHistory, Card
import random
from datetime import timedelta
from users.management.commands.generate_user_data import UserDataGenerator

fake = Faker()

class Command(BaseCommand):
    help = 'Generates dummy data for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of residents to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        self.generate_data(count)

    def generate_data(self, count):
        user_generator = UserDataGenerator(self.stdout, self.style)
        for _ in range(count):
            resident = user_generator.create_resident()
            self.create_invoices(resident)
            self.create_card(resident)
            user_generator.create_feedback(resident)

    def create_invoices(self, resident):
        for _ in range(random.randint(1, 5)):
            invoice = Invoice.objects.create(
                resident=resident,
                amount=round(random.uniform(10, 1000), 2),
                status=random.choice(['paid', 'unpaid'])
            )
            self.stdout.write(self.style.SUCCESS(f'Created invoice: {invoice}'))

            if invoice.status == 'paid':
                self.create_paid_history(resident, invoice)

    def create_paid_history(self, resident, invoice):
        paid_history = PaidHistory.objects.create(
            resident=resident,
            invoice=invoice,
            amount=invoice.amount,
            paid_at=fake.date_time_between(start_date=invoice.created_at, end_date=timezone.now())
        )
        self.stdout.write(self.style.SUCCESS(f'Created paid history: {paid_history}'))

    def create_card(self, resident):
        # First determine the card type
        card_type = random.choice(['visa', 'mastercard'])
        
        # Generate appropriate card number based on type
        if card_type == 'visa':
            # Visa cards start with 4 and are typically 16 digits
            card_no = '4' + ''.join([str(random.randint(0, 9)) for _ in range(15)])
        else:
            # Mastercard starts with 51-55 and are 16 digits
            card_no = str(random.randint(51, 55)) + ''.join([str(random.randint(0, 9)) for _ in range(14)])

        card = Card.objects.create(
            resident=resident,
            card_no=card_no,
            card_type=card_type,
            card_expiry=fake.future_date(end_date='+10y'),
            card_cvv=fake.credit_card_security_code(),
            card_name=resident.full_name,
            card_address=fake.street_address(),
            card_city=fake.city(),
            card_state=fake.state(),
            card_zip=fake.postcode(),
            card_country="Malaysia",
            card_phone=resident.phone_number,
            card_email=resident.email,
            card_dob=fake.date_of_birth(minimum_age=18, maximum_age=90),
            card_ssn=fake.ssn(),
            card_status=random.choice(['active', 'inactive']),
        )
        self.stdout.write(self.style.SUCCESS(f'Created card: {card}'))
