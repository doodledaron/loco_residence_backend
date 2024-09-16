# file: management/commands/finance_data_generator.py

from django.utils import timezone
from faker import Faker
from finances.models import Invoice, PaidHistory, Card
import random

fake = Faker()

class FinanceDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

    def generate_finance_data(self, residents):
        for resident in residents:  # Loop through each resident
            self.create_invoices(resident)
            self.create_card(resident)

    def create_invoices(self, resident):
        for _ in range(random.randint(1, 5)):
            invoice = Invoice.objects.create(
                resident=resident,
                amount=round(random.uniform(10, 1000), 2),
                status=random.choice(['paid', 'unpaid'])
            )
            self.stdout.write(self.style.SUCCESS(f'Created invoice: {invoice}'))

            if invoice.status == 'paid':
                self.create_paid_history(invoice)

    def create_paid_history(self, invoice):
        paid_history = PaidHistory.objects.create(
            invoice=invoice,
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
            card_status=random.choice(['active', 'inactive']),
        )
        self.stdout.write(self.style.SUCCESS(f'Created card: {card}'))
