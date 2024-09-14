from django.utils import timezone
from faker import Faker
from users.models import Resident
import random

fake = Faker()

class UserDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

    def generate_users(self, count):
        users = []
        for _ in range(count):
            user = self.create_resident()
            users.append(user)
        return users

    def create_resident(self):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = f"01{fake.numerify(text='#' * random.choice([8, 9]))}"

        resident = Resident.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email.lower(),
            phone_number=phone_number,
            full_name=f"{last_name} {first_name}",
            role=Resident.Role.RESIDENT
        )
        resident.set_password("testpassword123")
        resident.save()

        self.stdout.write(self.style.SUCCESS(f'Created resident: {resident}'))
        return resident
