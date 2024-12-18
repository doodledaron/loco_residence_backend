from collections import defaultdict
import datetime
from django.utils import timezone
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from bookings.models import Facility, FacilitySection, TimeSlot, Booking
from users.models import Resident
from .serializers import FacilitySerializer, TimeSlotSerializer, BookingSerializer
from rest_framework import status
from datetime import datetime, time


@api_view(['GET'])
def get_facilities(request):
    facilities = Facility.objects.all()
    serializer = FacilitySerializer(facilities, many=True)
    return Response(serializer.data)

#get the available time slots based on facility and date
@api_view(['GET'])
def get_available_time_slots(request, resident_id=None):
    facility_id = request.GET.get('facility_id')  # Get facility_id from request data
    date = request.GET.get('date')  # Get date from request data
    # Facility id and date must be provided
    if not facility_id or not date:
        return Response({"error": "Both facility and date are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Parse date as a naive date object
        date = datetime.strptime(date, '%Y-%m-%d')
        # Make it timezone-aware based on the system's timezone setting
        date = timezone.make_aware(date)
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    # Get facility
    try:
        facility = Facility.objects.get(pk=facility_id)
    except Facility.DoesNotExist:
        return Response({"error": "Facility not found."}, status=status.HTTP_404_NOT_FOUND)

    # Get all facility sections
    facility_sections = FacilitySection.objects.filter(facility=facility)

    # Get all time slots
    time_slots = TimeSlot.objects.all()

    # Get all bookings for the facility sections on the specified date
    bookings = Booking.objects.filter(booking_date=date, section__in=facility_sections)

    # Group bookings by time slot
    booked_slots_by_time = defaultdict(list)
    for booking in bookings:
        booked_slots_by_time[booking.time_slot.id].append(booking.section.id)

    # Find fully booked time slots (i.e., where all sections are booked)
    fully_booked_slots = []
    for time_slot_id, booked_sections in booked_slots_by_time.items():
        if len(booked_sections) == facility_sections.count():  # All sections are booked for this time slot
            fully_booked_slots.append(time_slot_id)

    # Get all available time slots (exclude those fully booked for all sections)
    available_time_slots = time_slots.exclude(id__in=fully_booked_slots)

    # Serialize the available time slots
    serializer = TimeSlotSerializer(available_time_slots, many=True)

    return Response(serializer.data)

#get the available facility sections based on facility, date and time slots
@api_view(['GET'])
def get_available_facility_sections(request):
    # Extract data from JSON request body
    facility = request.GET.get('facility_id')
    date = request.GET.get('date')
    time_slots = request.GET.getlist('time_slots')  # Use getlist to fetch multiple parameters

    # Validate that all required fields are present
    if not all([facility, date]) or not time_slots:  # Check for time_slots here
        return Response({"error": "Missing required parameters"}, status=400)
    
    # Ensure time_slots is a list of strings
    if not all(isinstance(slot, str) for slot in time_slots):
        return Response({"error": "Invalid time_slots format"}, status=400)
    
    # get the time slot based on the time slot list
    time_slots = TimeSlot.objects.filter(start_time__in=time_slots)

    # Get section IDs that are already booked for any of the specified time slots
    booked_section_ids = Booking.objects.filter(
        booking_date=date,
        time_slot__in=time_slots,  # Filter bookings based on the list of time slots
        section__facility=facility
    ).values_list('section_id', flat=True)
    
    # Get all sections for the facility
    all_sections = FacilitySection.objects.filter(facility=facility)
    
    # Exclude booked sections
    available_sections = all_sections.exclude(id__in=booked_section_ids)
    
    # Serialize the available sections (you may need to adjust the fields based on your model)
    available_sections_data = available_sections.values('id', 'section_name')  # Adjust fields as needed
    
    return Response(available_sections_data)


# book a facility section based on the facility, section, date and time slot
@api_view(['POST'])
def book_facility_section(request, resident_id):
    facility = request.data.get('facility_id')
    date = request.data.get('date')
    time_slots = request.data.get('time_slots', [])  # List of time slots in 'HH:MM:SS' format
    section = request.data.get('section_id')
    
    # Validate that all required fields are present
    if not all([facility, date, time_slots, section]):
        return Response({"error": "Missing required parameters"}, status=400)
    
    # Ensure time_slots is a list of strings
    if not isinstance(time_slots, list) or not all(isinstance(slot, str) for slot in time_slots):
        return Response({"error": "Invalid time_slots format"}, status=400)
    
    # get the time slot based on the time slot list
    time_slots = TimeSlot.objects.filter(start_time__in=time_slots)

    # Get the facility section based on section id
    try:
        section = FacilitySection.objects.get(id=section)
    except FacilitySection.DoesNotExist:
        return Response({"error": "Invalid section ID"}, status=400)
    

    # Check for any already booked slots
    booked_slots = []
    for time_slot in time_slots:
        if Booking.objects.filter(section=section, booking_date=date, time_slot=time_slot).exists():
            booked_slots.append(time_slot.start_time.strftime('%H:%M:%S'))
    
    if booked_slots:
        return Response({"error": f"Slots already booked: {', '.join(booked_slots)}, Please choose a time again"}, status=400)
    

    # Create bookings for all time slots
    bookings = []  # List to hold created booking instances
    for time_slot in time_slots:
        booking = Booking.objects.create(
            resident=Resident.objects.get(pk=resident_id),
            section=section,
            time_slot=time_slot,
            booking_date=date
        )
        bookings.append(booking)  # Add the booking to the list

    # Serialize booking details
    serializer = BookingSerializer(bookings, many=True)

    return Response({"message": "Booking successful", "bookings": serializer.data}, status=201)

#cancel a booking based on facility, date, time slots and section
@api_view(['POST', "DELETE"])
def cancel_booking(request, resident_id):
    booking_id = request.data.get('booking_id')  # Get facility_id from request data
    resident = Resident.objects.get(pk=resident_id) # Assuming the resident is already authenticated
    
    # Find bookings that match the criteria
    bookings_to_cancel = Booking.objects.filter(
        pk=booking_id,
        resident=resident
        
    )
    
    if not bookings_to_cancel.exists():
        return Response({"error": "No bookings found to cancel for the given parameters"}, status=404)
    
    canceled_booking = bookings_to_cancel.first()

    # Cancel bookings
    bookings_to_cancel.delete()

    return Response({"message": "Bookings canceled successfully", 
                     "canceled_booking" : {
                            "id": canceled_booking.id,
                            "section": canceled_booking.section.section_name,
                            "date": canceled_booking.booking_date,
                     }}, status=200)


#get all the bookings
@api_view(['GET'])
def get_all_bookings(request, resident_id):
    resident = Resident.objects.get(pk=resident_id)  # Assuming the resident is already authenticated
    bookings = Booking.objects.filter(
        resident=resident
    )
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

#get the booked time slots based on facility and date
@api_view(['GET'])
def get_booked_time_slots(request):
    facility_id = request.data.get('facility_id')  # Get facility_id from request data
    date = request.data.get('date')  # Get date from request data

    # Facility id and date must be provided
    if not facility_id or not date:
        return Response({"error": "Both facility and date are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Parse date as a naive date object
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    # Get facility
    try:
        facility = Facility.objects.get(pk=facility_id)
    except Facility.DoesNotExist:
        return Response({"error": "Facility not found."}, status=status.HTTP_404_NOT_FOUND)

    # Get all facility sections
    facility_sections = FacilitySection.objects.filter(facility=facility)

    # Get all bookings for the facility sections on the specified date
    bookings = Booking.objects.filter(booking_date=date, section__in=facility_sections)

    # Get a list of booked time slots
    booked_time_slots = bookings.values_list('time_slot', flat=True)

    # Get the actual TimeSlot objects for the booked time slots
    booked_time_slots_data = TimeSlot.objects.filter(id__in=booked_time_slots)

    # Serialize the booked time slots
    serializer = TimeSlotSerializer(booked_time_slots_data, many=True)
    
    return Response(serializer.data)


#expected call API flow
# user choose date -> call get_available_time_slots -> user choose time slot -> call get_available_facility_sections -> user choose section -> call book_facility_section


# @api_view(['GET'])
# #@permission_classes([IsAuthenticated])
# def get_user_bookings(request):
#     bookings = Booking.objects.filter(user=request.user)
#     serializer = BookingSerializer(bookings, many=True)
#     return Response(serializer.data)


