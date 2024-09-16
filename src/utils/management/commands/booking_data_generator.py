from django.utils import timezone
from datetime import timedelta, datetime
from bookings.models import Booking, FacilitySection
import random

class BookingDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

    def generate_bookings(self, residents, facilities, time_slots, num_bookings=30):
        start_date = timezone.now().date()
        booking_statuses = ['pending', 'approved', 'rejected']

        for _ in range(num_bookings):
            facility = random.choice(facilities)
            
            if not facility.booking_required:
                continue  # Skip facilities that don't require booking (e.g., gym)

            section = random.choice(facility.sections.all())
            time_slot = random.choice(time_slots)
            resident = random.choice(residents)
            booking_date = start_date + timedelta(days=random.randint(0, 30))
            booking_status = 'approved'

            if not Booking.objects.filter(section=section, booking_date=booking_date, time_slot=time_slot).exists():
                booking = Booking.objects.create(
                    resident=resident,
                    section=section,
                    time_slot=time_slot,
                    booking_date=booking_date,
                    booking_status=booking_status
                )
                self.stdout.write(self.style.SUCCESS(
                                f'Created booking for {resident.email} at {section.facility.name} - {section.section_name} '
                                f'on {booking_date} (Date), Status: {booking_status}'
                            ))

    def generate_all_bookings(self, residents, facilities, time_slots, num_bookings=30):
        self.generate_bookings(residents, facilities, time_slots, num_bookings)
        self.stdout.write(self.style.SUCCESS('All booking data generated successfully!'))