from django.db import models
from users.models import Resident



class FacilityType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        #explicitly set the plural and singular name of the model
        verbose_name = "Facility Type"
        verbose_name_plural = "Facility Types"

class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_units = models.PositiveIntegerField(default=1)
    facility_type = models.ForeignKey(FacilityType, on_delete=models.CASCADE)  # Add this field

    def __str__(self):
        return f"{self.name} ({self.facility_type.name})"

    class Meta:
        verbose_name_plural = "Facilities"

class TimeSlot(models.Model):
    start_time = models.TimeField()
    duration = models.DecimalField(max_digits=4, decimal_places=2)  # in hours

    def __str__(self):
        return f"{self.start_time} ({self.duration} hours)"
    

class Booking(models.Model):
    user = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='bookings')
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, related_name='bookings')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name='bookings')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    #Meta class inside a model is used to provide metadata to the model
    #defines options that aren't directly related to the fields but affect the model's behavior
    class Meta:
        #ensures that for a given facility, date, and time slot must be unique --> no double booking
        unique_together = ['facility', 'date', 'time_slot']

    def __str__(self):
        return f"{self.user.username} - {self.facility.name} on {self.date} at {self.time_slot.start_time}"

