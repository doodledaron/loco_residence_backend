from django.utils import timezone
from bookings.models import FacilityType, Facility, TimeSlot

class FacilityDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

    def generate_facilities(self):
        facility_types = self.create_facility_types()
        return self.create_facilities(facility_types)

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
        facilities = []
        for ft in facility_types:
            facility = Facility.objects.create(name=f"{ft.name}s", facility_type=ft, total_units=3)
            facilities.append(facility)
            self.stdout.write(self.style.SUCCESS(f'Created facility: {facility.name}'))
        return facilities

    def generate_time_slots(self):
        time_slots = []
        for hour in range(8, 23):  # 8 AM to 11 PM
            for minute in [0, 30]:
                time_slot = TimeSlot.objects.create(
                    start_time=f"{hour:02d}:{minute:02d}:00",
                    duration=0.5
                )
                time_slots.append(time_slot)
                self.stdout.write(self.style.SUCCESS(f'Created time slot: {time_slot.start_time}'))
        return time_slots