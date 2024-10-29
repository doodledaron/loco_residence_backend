import base64
from datetime import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from users.models import Resident
from .models import Complaint
from .serializers import ComplaintSerializer
# Create your views here.

@api_view(['POST'])
def create_complaint(request, resident_id):
    title = request.data.get('title')
    description = request.data.get('description')
    date = request.data.get('date')
    image = request.FILES.get('image')

    # Validate required fields
    if not all([title, description, date]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate resident existence
    try:
        resident = Resident.objects.get(pk=resident_id)
    except Resident.DoesNotExist:
        return Response({'error': 'Resident not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Convert ISO 8601 datetime to date
    try:
        date = datetime.fromisoformat(date).date()
    except ValueError:
        return Response({'error': 'Invalid date format. Expected ISO 8601 format.'}, status=status.HTTP_400_BAD_REQUEST)

    complaint = Complaint(
        resident=resident,
        title=title,
        description=description,
        date=date,
    )

    if image:
        complaint.image = image

    complaint.save()
    serializer = ComplaintSerializer(complaint)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_all_complaints(request, resident_id):
    # Validate resident existence
    try:
        resident = Resident.objects.get(pk=resident_id)
    except Resident.DoesNotExist:
        return Response({'error': 'Resident not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        complaints = Complaint.objects.filter(resident=resident).order_by('-date')
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Complaint.DoesNotExist:
        return Response({'error': 'No complaints found'}, status=status.HTTP_404_NOT_FOUND)