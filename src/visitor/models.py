from django.db import models

from django.apps import apps
from users.models import Resident

# Create your models here.
class Visitor(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='visitors', null=True)
    full_name = models.CharField(max_length=100)
    hp_number = models.CharField(max_length=100)
    car_plate_no = models.CharField(max_length=100)
    check_in_date = models.DateField(auto_now_add=False)
    check_out_date = models.DateField(auto_now_add=False, null=True)
    check_in_time = models.TimeField(auto_now_add=False, null=True)
    check_out_time = models.TimeField(auto_now_add=False, null=True)
    purpose_of_visit = models.CharField(max_length=100)

    @property
    def visitor_model(self):
        return apps.get_model('parking', 'VisitorParking')
    