from rest_framework import serializers
from .models import Facility, Booking, TimeSlot

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'

#You can add available_units as a custom field by using SerializerMethodField in your TimeSlotSerializer and update the view accordingly.
class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'duration',]


class BookingSerializer(serializers.ModelSerializer):
    facility = FacilitySerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'user', 'facility', 'time_slot', 'date']


