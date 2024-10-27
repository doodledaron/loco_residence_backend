from django.db import models

from users.models import Resident

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Received', 'Received'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='complaints', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Received')
    date = models.DateField()  # Use DateField for date only
    complaint_created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='complaints/', null=True, blank=True)  # Optional image field

    def __str__(self):
        return f"{self.title} - {self.status}"
