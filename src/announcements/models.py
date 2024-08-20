from django.utils import timezone
from django.db import models
from django.apps import apps 
from users.models import CustomUser

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.PROTECT)
    
    #in front end, must add an image
    image = models.ImageField(upload_to='announcements/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

        