from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ('resident', 'card_created_at', 'card_updated_at', 'card_deleted_at')