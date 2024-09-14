from rest_framework import serializers
from .models import FacilityType, Facility, Booking, TimeSlot

class FacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityType
        fields = '__all__'

class FacilitySerializer(serializers.ModelSerializer):
    facility_type = FacilityTypeSerializer(read_only=True)
    class Meta:
        model = Facility
        fields = '__all__'

#You can add available_units as a custom field by using SerializerMethodField in your TimeSlotSerializer and update the view accordingly.
class TimeSlotSerializer(serializers.ModelSerializer):
    available_units = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'duration', 'available_units']

    def get_available_units(self, obj):
        # 'obj' here is the actual TimeSlot instance passed
        return obj.available_units

class BookingSerializer(serializers.ModelSerializer):
    facility = FacilitySerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'