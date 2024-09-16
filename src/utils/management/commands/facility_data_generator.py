from datetime import time
from bookings.models import Facility, FacilitySection, TimeSlot

class FacilityDataGenerator:
    def __init__(self, stdout, style):
        self.stdout = stdout
        self.style = style

    def generate_facilities(self):
        facility_data = [
            {"name": "Pickle Ball Court", "description": "Court for playing pickle ball", "booking_required": True},
            {"name": "Meeting Room", "description": "Room for meetings and events", "booking_required": True},
            {"name": "Gym", "description": "Fitness center for residents", "booking_required": False}
        ]
        facilities = []
        for data in facility_data:
            facility = Facility.objects.create(**data)
            facilities.append(facility)
            self.stdout.write(self.style.SUCCESS(f'Created facility: {facility.name}'))
            
            if facility.booking_required:
                self.generate_facility_sections(facility)
        
        return facilities

    def generate_facility_sections(self, facility):
        for i in range(1, 4):  # Create 3 sections for each bookable facility
            section = FacilitySection.objects.create(
                facility=facility,
                section_name=f"{facility.name} Section {i}",
                is_available=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created facility section: {section.section_name}'))

    def generate_time_slots(self):
        time_slots = []
        start_hour, end_hour = 8, 22  # 8 AM to 10 PM

        for hour in range(start_hour, end_hour + 1):
            for minute in [0, 30]:
                start_time = time(hour=hour, minute=minute)
                end_time = time(hour=hour, minute=minute + 30) if minute == 0 else time(hour=hour + 1, minute=0)
                
                if end_time <= time(hour=end_hour, minute=0):
                    time_slot = TimeSlot.objects.create(
                        start_time=start_time,
                        end_time=end_time
                    )
                    time_slots.append(time_slot)
                    self.stdout.write(self.style.SUCCESS(f'Created time slot: {time_slot.start_time} - {time_slot.end_time}'))

        return time_slots

    def generate_all_data(self):
        self.generate_facilities()
        self.generate_time_slots()
        self.stdout.write(self.style.SUCCESS('All facility data generated successfully!'))