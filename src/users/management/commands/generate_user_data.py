# file: management/commands/user_data_generator.py

from django.utils import timezone
from faker import Faker
from users.models import Resident, Feedback
import random

fake = Faker()

class UserDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

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

    def create_feedback(self, resident):
        feedback = Feedback.objects.create(
            resident_id=resident,
            description=fake.text(max_nb_chars=200),
            rating=random.randint(1, 5),
        )
        self.stdout.write(self.style.SUCCESS(f'Created feedback: {feedback}'))