from django.db import models
from users.models import Resident

class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    booking_required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} booking required: {self.booking_required}"

    class Meta:
        verbose_name_plural = "Facilities"

class FacilitySection(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='sections')
    section_name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.section_name} is available: {self.is_available}"

    class Meta:
        verbose_name_plural = "Facility Sections"

class TimeSlot(models.Model):
    #duration per time slot is half an hour in defailt
    start_time = models.TimeField()
    end_time = models.TimeField()
    

    def __str__(self):
        return f"{self.start_time}"
    


class Booking(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='bookings')
    section = models.ForeignKey(FacilitySection, on_delete=models.PROTECT, related_name='bookings')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name='bookings')
    booking_date = models.DateTimeField()
    booking_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    #rmb to check how booking_status works
    class Meta:
        #ensures that for a given facility, date, and time slot must be unique --> no double booking
        unique_together = ['section', 'booking_date', 'time_slot']

    def __str__(self):
        return f"{self.resident.username} - {self.section.facility.name} on {self.booking_date} at {self.time_slot.start_time}"



