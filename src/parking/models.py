from django.db import models
from residence.models import Block
from users.models import Resident
from django.apps import apps
from visitor.models import Visitor

class Parking(models.Model):
    block = models.ForeignKey(Block, on_delete=models.PROTECT, related_name='parkings', null=True)
    parking_no = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft deletion field

    def __str__(self):
        return self.parking_no

    #indexing for faster queries
    class Meta:
        indexes = [
            models.Index(fields=['parking_no']),
        ]


class ResidentParking(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.PROTECT, related_name='resident_parkings', null=True)
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='resident_parkings', null=True)
    is_occupied = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft deletion field

    def __str__(self):
        return f"Resident Parking number {self.parking}"


class VisitorParking(models.Model):
    #visitor.Visitor to avoid circular import
    visitor = models.OneToOneField(Visitor, on_delete=models.PROTECT, related_name='visitors_parkings', null=True)
    parking = models.ForeignKey(Parking, on_delete=models.PROTECT, related_name='visitor_parkings', null=True)  # Updated related_name for clarity
    is_occupied = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft deletion field

    def __str__(self):
        return f"Visitor Parking number {self.parking}"
    
    #apps.get_model to avoid circular import
    @property
    def visitor_model(self):
        return apps.get_model('visitor', 'Visitor')