from django.db import models
from users.models import Resident

class Residence(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} in {self.city}, {self.state}"
    
class Block(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.PROTECT, related_name='blocks', null=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Unit(models.Model):
    resident = models.ForeignKey(Resident,on_delete=models.PROTECT, related_name='units', null=True)
    block = models.ForeignKey(Block, on_delete=models.PROTECT, related_name='units',null=True)
    unit_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('unit_no', 'block')


    def __str__(self):
        return self.unit_no