from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'image']
        read_only_fields = ['created_at', 'updated_at']