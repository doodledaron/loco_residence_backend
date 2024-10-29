from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from users.models import Resident
from visitor.models import Visitor
from visitor.serializers import VisitorSerializer
from django.utils import timezone
from django.utils import timezone
from datetime import datetime
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Visitor
from .serializers import VisitorSerializer
from django.utils.timezone import localtime

# View all visitors
@api_view(['GET'])
def view_all_visitors(request, resident_id=None):  # Make resident_id optional
    if resident_id:  # Check if resident_id is provided
        try:
            resident = Resident.objects.get(pk=resident_id)
            visitors = Visitor.objects.filter(resident=resident)
        except Resident.DoesNotExist:
            return Response({'error': 'Resident not found'}, status=404)
    else:
        visitors = Visitor.objects.all()  # Get all visitors if resident_id is not provided

    serializer = VisitorSerializer(visitors, many=True)
    return Response(serializer.data)


# Django API modification
@api_view(['POST'])
def register_visitor(request, resident_id):
    # Get visitor details from the request
    full_name = request.data.get('full_name')
    hp_number = request.data.get('hp_number')
    car_plate_no = request.data.get('car_plate_no')
    check_in_date = request.data.get('check_in_date')
    purpose_of_visit = request.data.get('purpose_of_visit')

    if not all([
        full_name,
        hp_number,
        car_plate_no,
        check_in_date,
        purpose_of_visit
    ]):
        return Response({'error': 'All fields are required'}, status=400)

    # Verify resident exists
    try:
        resident = Resident.objects.get(pk=resident_id)
    except Resident.DoesNotExist:
        return Response({'error': 'Resident not found'}, status=404)

    # Parse check_in_date as a naive datetime (without time)
    parsed_datetime = datetime.strptime(check_in_date, "%Y-%m-%d")
    
    # Ensure the check_in_datetime is timezone-aware
    check_in_datetime = timezone.make_aware(parsed_datetime) if timezone.is_naive(parsed_datetime) else parsed_datetime
    check_in_date_only = check_in_datetime.date()

    # Check for duplicate visitor
    duplicate_visitor = Visitor.objects.filter(
        resident=resident,
        full_name=full_name,
        hp_number=hp_number,
        car_plate_no=car_plate_no,
        check_in_date=check_in_date_only,
        purpose_of_visit=purpose_of_visit
    ).exists()

    if duplicate_visitor:
        return Response({'error': 'Visitor with these details already exists'}, status=400)

    # Create visitor
    visitor = Visitor(
        resident=resident,
        full_name=full_name,
        hp_number=hp_number,
        car_plate_no=car_plate_no,
        check_in_date=check_in_date_only,
        purpose_of_visit=purpose_of_visit
    )
    visitor.save()

    serializer = VisitorSerializer(visitor)
    return Response({
        'message': 'Visitor registered successfully',
        'visitor': serializer.data
    }, status=201)



# update visitor details
@api_view(['POST'])
def update_visitor_details(request):
    visitor_id = request.data.get('visitor_id')
    full_name = request.data.get('full_name')
    hp_number = request.data.get('hp_number')
    car_plate_no = request.data.get('car_plate_no')
    purpose_of_visit = request.data.get('purpose_of_visit')

    if not visitor_id:
        return Response({
            'error': 'Visitor ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        visitor = Visitor.objects.get(pk=visitor_id)
        
        # Update visitor details
        if full_name:
            visitor.full_name = full_name
        if hp_number:
            visitor.hp_number = hp_number
        if car_plate_no:
            visitor.car_plate_no = car_plate_no
        if purpose_of_visit:
            visitor.purpose_of_visit = purpose_of_visit
        
        visitor.save()
        
        serializer = VisitorSerializer(visitor)
        return Response({
            'message': 'Visitor details updated successfully',
            'visitor': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Visitor.DoesNotExist:
        return Response({
            'error': 'Visitor not found'
        }, status=status.HTTP_404_NOT_FOUND)

# check in visitor
@api_view(['POST'])
def check_in_visitor(request):
    visitor_id = request.data.get('visitor_id')
    
    if not visitor_id:
        return Response({
            'error': 'Visitor ID is required'
        }, status=400)
    
    try:
        visitor = Visitor.objects.get(pk=visitor_id)
        
        # Check if visitor is already checked in
        if visitor.check_in_time:
            return Response({
                'error': 'Visitor is already checked in'
            }, status=400)
        
        # Get current time and format it
        current_time = localtime(timezone.now())
        formatted_time = current_time.strftime('%H:%M:%S')
        formatted_time = datetime.strptime(formatted_time, '%H:%M:%S').time()
        
        # Update visitor check-in details
        visitor.check_in_time = formatted_time
        visitor.save()
        
        serializer = VisitorSerializer(visitor)
        return Response({
            'message': 'Visitor checked in successfully',
            'visitor': serializer.data
        }, status=200)
        
    except Visitor.DoesNotExist:
        return Response({
            'error': 'Visitor not found'
        }, status=404)

# check out visitor
@api_view(['POST'])
def check_out_visitor(request):
    visitor_id = request.data.get('visitor_id')
    
    if not visitor_id:
        return Response({
            'error': 'Visitor ID is required'
        }, status=400)
    
    try:
        visitor = Visitor.objects.get(pk=visitor_id)
        
        # Check if visitor is already checked out
        if visitor.check_out_time and visitor.check_out_date:
            return Response({
                'error': 'Visitor is already checked out'
            }, status=400)
        
        # Get current datetime and format time
        current_datetime = localtime(timezone.now())
        formatted_time = current_datetime.strftime('%H:%M:%S')
        formatted_time = datetime.strptime(formatted_time, '%H:%M:%S').time()
        
        # Update visitor check-out details
        visitor.check_out_time = formatted_time
        visitor.check_out_date = current_datetime.date()
        visitor.save()
        
        serializer = VisitorSerializer(visitor)
        return Response({
            'message': 'Visitor checked out successfully',
            'visitor': serializer.data
        }, status=200)
        
    except Visitor.DoesNotExist:
        return Response({
            'error': 'Visitor not found'
        }, status=404)