from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import FacilityType, Facility, TimeSlot, Booking
from django.utils import timezone
from datetime import timedelta
from faker import Faker
import random
from users.models import Resident

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating fake data...')

        # Create facility types
        facility_types = self.create_facility_types()

        # Create facilities
        self.create_facilities(facility_types)

        # Create time slots
        self.create_time_slots()

        # Create residents (users)
        users = self.create_residents()

        # Create bookings
        self.create_bookings(users)

        self.stdout.write(self.style.SUCCESS('Fake data generated successfully'))

    def create_facility_types(self):
        facility_types = [
            FacilityType.objects.create(name="Pickle Ball Court"),
            FacilityType.objects.create(name="Meeting Room"),
            FacilityType.objects.create(name="Event Hall")
        ]
        for ft in facility_types:
            self.stdout.write(self.style.SUCCESS(f'Created facility type: {ft.name}'))
        return facility_types

    def create_facilities(self, facility_types):
        for ft in facility_types:
            facility = Facility.objects.create(name=f"{ft.name}s", facility_type=ft, total_units=3)
            self.stdout.write(self.style.SUCCESS(f'Created facility: {facility.name}'))

    def create_time_slots(self):
        for hour in range(8, 23):  # 8 AM to 11 PM
            for minute in [0, 30]:
                time_slot = TimeSlot.objects.create(
                    start_time=f"{hour:02d}:{minute:02d}:00",
                    duration=0.5
                )
                self.stdout.write(self.style.SUCCESS(f'Created time slot: {time_slot.start_time}'))

    # def create_residents(self):
    #     first_name = fake.first_name()
    #     last_name = fake.last_name()
    #     email = fake.email()
    #     phone_number = f"01{fake.numerify(text='#' * random.choice([8, 9]))}"  # Malaysian phone format
    #     residents = [
    #         Resident.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             email=email.lower(),
    #             phone_number=phone_number,
    #             full_name=f"{last_name} {first_name}",
    #             role=Resident.Role.RESIDENT
    #         )
    #         for i in range(1, 6)
    #     ]


    #     for resident in residents:
    #         resident.set_password("testpassword123")  # Set a default password
    #         resident.save()
    #         self.stdout.write(self.style.SUCCESS(f'Created resident: {resident.username}'))
    #     return residents

    def create_bookings(self, resident):
        facilities = Facility.objects.all()
        time_slots = TimeSlot.objects.all()
        start_date = timezone.now().date()

        for _ in range(30):  # Create 30 random bookings
            facility = random.choice(facilities)
            time_slot = random.choice(time_slots)
            user = random.choice(resident)
            date = start_date + timedelta(days=random.randint(0, 30))

            # Check if booking already exists
            if not Booking.objects.filter(facility=facility, date=date, time_slot=time_slot).exists():
                booking = Booking.objects.create(
                    user=user,
                    facility=facility,
                    date=date,
                    time_slot=time_slot
                )
                self.stdout.write(self.style.SUCCESS(f'Created booking for {user.username} at {facility.name} on {date} during {time_slot.start_time}'))
