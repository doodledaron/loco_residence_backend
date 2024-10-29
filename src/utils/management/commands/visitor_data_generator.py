import random
from datetime import datetime, timedelta
from visitor.models import Visitor
from faker import Faker

fake = Faker()

class VisitorDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

    def generate_visitors(self, residents):
        for resident in residents:
            for _ in range(random.randint(1, 5)):  # Each resident has 1 to 5 visitors
                visitor = Visitor.objects.create(
                    resident=resident,
                    full_name=fake.name(),
                    hp_number=fake.phone_number(),
                    car_plate_no=fake.license_plate_car(),
                    check_in_date=datetime.now().date(),
                    check_out_date=datetime.now().date() + timedelta(days=random.randint(1, 7)),
                    check_in_time=datetime.now().time(),
                    check_out_time=(datetime.now() + timedelta(hours=random.randint(1, 4))).time(),
                    purpose_of_visit=random.choice(["Visitor", "Delivery", "Constructor"])
                )
                self.stdout.write(self.style.SUCCESS(f'Created visitor: {visitor.full_name} for resident: {resident}'))
