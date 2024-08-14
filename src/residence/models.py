from django.db import models
from users.models import Resident

class Residence(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Block(models.Model):
    name = models.CharField(max_length=100)
    residence_id = models.ForeignKey(Residence, on_delete=models.PROTECT, related_name='blocks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Unit(models.Model):
    unit_no = models.CharField(max_length=100)
    resident_id = models.ForeignKey(Resident,on_delete=models.PROTECT, related_name='units', null=True)
    block_id = models.ForeignKey(Block, on_delete=models.PROTECT, related_name='units',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name