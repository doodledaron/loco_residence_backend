from django.utils import timezone
from datetime import timedelta
from bookings.models import Booking
import random

class BookingDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

    def generate_bookings(self, users, facilities, time_slots, num_bookings=30):
        start_date = timezone.now().date()

        for _ in range(num_bookings):
            facility = random.choice(facilities)
            time_slot = random.choice(time_slots)
            user = random.choice(users)
            date = start_date + timedelta(days=random.randint(0, 30))

            if not Booking.objects.filter(facility=facility, date=date, time_slot=time_slot).exists():
                booking = Booking.objects.create(
                    user=user,
                    facility=facility,
                    date=date,
                    time_slot=time_slot
                )
                self.stdout.write(self.style.SUCCESS(f'Created booking for {user.full_name} at {facility.name} on {date} during {time_slot.start_time}'))