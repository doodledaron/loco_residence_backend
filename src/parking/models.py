from django.db import models
from residence.models import Block, Unit
from residents.models import Resident

# # Create your models here.
# class Parking(models.Model):
#     block_id = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='parkings')
#     unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='parkings')

#     parking_created_at = models.DateTimeField(auto_now_add=True)
#     parking_updated_at = models.DateTimeField(auto_now=True)
#     parking_deleted_at = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return self.parking_no
    
# # class ResidentParking(models.Model):
    
