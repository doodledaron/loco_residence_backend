from django.contrib import admin
from .models import FacilityType, Facility, TimeSlot, Booking
# Register your models here.

@admin.register(FacilityType)
class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'total_units')
    list_filter = ('facility_type',)
    search_fields = ('name',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'duration')
    list_filter = ('duration',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'facility', 'date', 'time_slot', 'created_at')
    list_filter = ('facility__facility_type', 'date')  # Nested relationship (facility > facility_type)
    search_fields = ('user__username', 'facility__name')  # Nested relationship (user > user_name)
    date_hierarchy = 'date'