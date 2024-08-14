from django.db import models

from parking.models import VisitorParking

# Create your models here.
class Visitor(models.Model):
    full_name = models.CharField(max_length=100)
    hp_number = models.CharField(max_length=100)
    car_plate_no = models.CharField(max_length=100)
    check_in_date = models.DateTimeField(auto_now_add=False)
    check_out_date = models.DateTimeField(auto_now_add=False, null=True)
    check_in_time = models.DateTimeField(auto_now_add=False)
    check_out_time = models.DateTimeField(auto_now_add=False, null=True)
    purpose_of_visit = models.CharField(max_length=100)
    parking_id = models.OneToOneField(VisitorParking, on_delete=models.CASCADE, related_name='visitor_id')
    