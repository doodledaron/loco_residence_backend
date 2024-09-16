import datetime
from django.utils import timezone
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from bookings.models import Facility, FacilitySection, TimeSlot, Booking
from bookings.utils import get_time_slot_ids
from users.models import Resident
from .serializers import FacilitySerializer, TimeSlotSerializer, BookingSerializer
from rest_framework import status
from datetime import datetime, time


@api_view(['GET'])
def get_facilities(request):
    facilities = Facility.objects.all()
    serializer = FacilitySerializer(facilities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_available_slots(request):
    facility_id = request.data.get('facility_id')  # Get facility_id from request data
    date = request.data.get('date')  # Get date from request data
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
    bookings = Booking.objects.filter(booking_date=date)

    # Serialize the result
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def create_booking(request):
    #get request data in json
    resident_id = request.data.get('resident_id')  # Get user_id from request data
    start_time_list = request.data.get('start_time_list')  # Get start_time_list from request data
    facility_id = request.data.get('facility_id')  # Get facility_id from request data
    date = request.data.get('date')  # Get date from request data


    if not resident_id:
        return Response({"error": "Resident ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        resident = Resident.objects.get(id=resident_id)
    except Resident.DoesNotExist:
        return Response({"error": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Ensure all required fields are provided
    if not all([facility_id, date, start_time_list]):
        return Response({"error": "Facility, date and time slot are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        facility = Facility.objects.get(id=facility_id)
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    except Facility.DoesNotExist:
        return Response({"error": "Invalid facility."}, status=status.HTTP_400_BAD_REQUEST)

    responses = []
    #book each time slot individually
    for start_time in start_time_list:
        try:
            time_slot = TimeSlot.objects.get(start_time=start_time)  # Assuming `start_time` is a unique field
        except TimeSlot.DoesNotExist:
            responses.append({"start_time": start_time, "error": "Invalid time slot."})
            continue

        # Check if the slot is already booked
        if Booking.objects.filter(facility=facility, date=date, time_slot=time_slot).exists():
            responses.append({"start_time": start_time, "error": "Slot is already booked."})
            continue
        
        # Check if there are available units for the slot
        booked_count = Booking.objects.filter(facility=facility, date=date, time_slot=time_slot).count()
        if booked_count >= facility.total_units:
            responses.append({"start_time": start_time, "error": "No available units for this slot."})
            continue
        
        # Create booking
        booking = Booking.objects.create(
            user=resident,
            facility=facility,
            time_slot=time_slot,
            date=date
        )

        serializer = BookingSerializer(booking)
        responses.append({"start_time": start_time, "booking": serializer.data})

    # Return a summary of the booking results
    if any("error" in response for response in responses):
        return Response(responses, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(responses, status=status.HTTP_201_CREATED)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


