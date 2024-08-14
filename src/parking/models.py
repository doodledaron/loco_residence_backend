from django.db import models
from residence.models import Block, Unit
from users.models import Resident

# Create your models here.
class Parking(models.Model):
    block_id = models.ForeignKey(Block, on_delete=models.PROTECT, related_name='parkings')

    parking_created_at = models.DateTimeField(auto_now_add=True)
    parking_updated_at = models.DateTimeField(auto_now=True)
    parking_deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.parking_no
    
class ResidentParking(models.Model):
    slot_no = models.CharField(max_length=100)
    parking_id = models.ForeignKey(Parking, on_delete=models.PROTECT, related_name='resident_parkings')
    resident_id = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='resident_parkings')
    is_occupied = models.BooleanField(default=False)
    
class VisitorParking(models.Model):
    slot_no = models.CharField(max_length=100)
    parking_id = models.ForeignKey(Parking, on_delete=models.PROTECT, related_name='parking')
    is_occupied = models.BooleanField(default=False)
    
    
