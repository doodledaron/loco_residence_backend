from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from users.models import Resident, Feedback
from finances.models import Invoice, PaidHistory, Card
import random
from datetime import timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Generates dummy data for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of residents to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        self.generate_data(count)

    def generate_data(self, count):
        for _ in range(count):
            resident = self.create_resident()
            self.create_invoices(resident)
            self.create_card(resident)
            self.create_feedback(resident)

    def create_resident(self):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = f"01{fake.numerify(text='#' * random.choice([8, 9]))}"  # Malaysian phone format

        resident = Resident.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email.lower(),
            phone_number=phone_number,
            full_name=f"{last_name} {first_name}",
            role=Resident.Role.RESIDENT
        )
        resident.set_password("testpassword123")  # Set a default password
        resident.save()

        self.stdout.write(self.style.SUCCESS(f'Created resident: {resident}'))
        return resident

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
        card = Card.objects.create(
            resident=resident,
            card_no=fake.credit_card_number(),
            card_type=random.choice(['visa', 'mastercard', 'amex']),
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
            card_ssn=fake.ssn(),  # Note: Malaysia doesn't use SSN, you might want to replace this
            card_status=random.choice(['active', 'inactive']),
        )
        self.stdout.write(self.style.SUCCESS(f'Created card: {card}'))

    def create_feedback(self, resident):
        feedback = Feedback.objects.create(
            resident_id=resident,
            description=fake.text(max_nb_chars=200),
            rating=random.randint(1, 5),
        )
        self.stdout.write(self.style.SUCCESS(f'Created feedback: {feedback}'))