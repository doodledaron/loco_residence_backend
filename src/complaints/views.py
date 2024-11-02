import base64
from datetime import datetime
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
import os
from users.models import Resident
from PIL import Image
import google.generativeai as genai
from .models import Complaint
from .serializers import ComplaintSerializer
# Create your views here.


# Initialize Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

TEXT_ANALYSIS_PROMPT = '''
Analyze this complaint title and description and respond ONLY with a JSON object in the following format, nothing else:
{
    "has_inappropriate_content": boolean,
    "is_valid_complaint": boolean
}

Guidelines for analysis:
- Set has_inappropriate_content to true if the text contains: hate speech, profanity, explicit content, threats, or harassment
- Set is_valid_complaint to false if the text is: spam, promotional content, or unrelated to residential issues

Respond only with the JSON object, no additional text or explanations.
Example response:
{
    "has_inappropriate_content": false,
    "is_valid_complaint": true
}
'''

IMAGE_ANALYSIS_PROMPT = '''
Analyze this complaint image and provide a response in the following JSON format:
{
    "image_is_relevant": boolean,
    "has_inappropriate_content": boolean
}

Consider the following:
1. Relevance: Does the image directly relate to the complaint title and description?
2. Appropriateness: Is there any inappropriate or sensitive content?

Return false for image_is_relevant if the image is:
- Blurry/unreadable
- Completely unrelated to the complaint
- Too dark/bright to see details

Return true for has_inappropriate_content if the image contains:
- Explicit content
- Violence
- Offensive gestures or symbols
- Other inappropriate material
'''

@api_view(['POST'])
def create_complaint(request, resident_id):
    try:
        # Validate basic fields first
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
            return Response({'error': 'Invalid date format. Expected ISO 8601 format.'}, 
                        status=status.HTTP_400_BAD_REQUEST)

        # Text content analysis
        try:
            text_content = f"Title: {title}\nDescription: {description}"
            text_response = model.generate_content([
                TEXT_ANALYSIS_PROMPT,
                text_content
            ])
            
            text_analysis = json.loads(text_response.text)
            
            if text_analysis.get('has_inappropriate_content'):
                return Response({
                    'error': 'The complaint contains inappropriate content'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not text_analysis.get('is_valid_complaint'):
                return Response({
                    'error': 'The complaint appears to be invalid or spam'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': f'Error analyzing complaint text: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Image processing with enhanced error handling
        if image:
            try:
                # Validate image file type
                valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
                ext = os.path.splitext(image.name)[1].lower()
                if ext not in valid_extensions:
                    return Response({
                        'error': f'Invalid image format. Supported formats: {", ".join(valid_extensions)}'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Validate image size (e.g., max 10MB)
                if image.size > 10 * 1024 * 1024:  # 10MB in bytes
                    return Response({
                        'error': 'Image size too large. Maximum size is 10MB'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Process image with PIL
                try:
                    with Image.open(image) as img:
                        # Verify it's actually an image
                        img.verify()
                        
                        # Reset file pointer after verify
                        image.seek(0)
                        
                        # Reopen for content analysis
                        img = Image.open(image)
                        
                        # Generate response from Gemini
                        image_response = model.generate_content([
                            IMAGE_ANALYSIS_PROMPT,
                            img,
                            f"Title: {title}\nDescription: {description}"
                        ])
                        
                        image_analysis = json.loads(image_response.text)
                        
                        if not image_analysis.get('image_is_relevant'):
                            return Response({
                                'error': 'The uploaded image is not relevant to the complaint or is of poor quality'
                            }, status=status.HTTP_400_BAD_REQUEST)
                        
                        if image_analysis.get('has_inappropriate_content'):
                            return Response({
                                'error': 'The uploaded image contains inappropriate content'
                            }, status=status.HTTP_400_BAD_REQUEST)
                
                except (IOError, SyntaxError) as e:
                    return Response({
                        'error': 'Invalid or corrupted image file'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except Exception as e:
                return Response({
                    'error': f'Error processing image: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Create and save complaint if all validations pass
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

    except Exception as e:
        # Log the full error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error in create_complaint: {str(e)}", exc_info=True)
        
        return Response({
            'error': 'An unexpected error occurred while processing your request'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET'])
def view_resident_complaints(request, resident_id):
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
    

@api_view(['GET'])
def view_all_complaints(request):

    try:
        complaints = Complaint.objects.all().order_by('-date')
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Complaint.DoesNotExist:
        return Response({'error': 'No complaints found'}, status=status.HTTP_404_NOT_FOUND)