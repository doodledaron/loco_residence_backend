import base64
from datetime import datetime, timedelta
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
from .serializers import ComplaintSerializer, SimilarComplaintSerializer

# Constants for error messages
ERROR_MESSAGES = {
    'category_analysis': 'Error analyzing complaint category: {}',
    'similarity_check': 'Error checking for similar complaints: {}'
}


# Initialize Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash', generation_config=genai.types.GenerationConfig(response_mime_type="application/json",max_output_tokens=2048))

#initialize logger
import logging
logger = logging.getLogger(__name__)

TEXT_ANALYSIS_PROMPT = '''
Analyze this complaint and respond ONLY with a valid JSON object:

COMPLAINT:
Title: {title}
Description: {description}

RESPOND WITH THIS EXACT JSON STRUCTURE:
{{
    "has_inappropriate_content": boolean,
    "is_valid_complaint": boolean,
    "reason": string
}}

Guidelines for analysis:
- Set has_inappropriate_content to true if the text contains: hate speech, profanity, explicit content, threats, or harassment
- Set is_valid_complaint to false if the title and description content has a mismatch or is not related to each other

Return ONLY the JSON object, no additional text, comments, or markdown formatting.
'''

IMAGE_ANALYSIS_PROMPT = '''
Analyze this complaint image:

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

RESPOND WITH THIS EXACT JSON STRUCTURE:
{{
    "image_is_relevant": boolean,
    "has_inappropriate_content": boolean
}}
'''


# Updated prompts with clearer structure and explicit formatting
CATEGORY_ANALYSIS_PROMPT = '''
Analyze this complaint and respond ONLY with a JSON object, no other text:

COMPLAINT:
Title: {title}
Description: {description}
Current Category: {category}

VALID CATEGORIES:
- Facility
- Payment
- Bookings
- Services
- Other

RESPOND WITH THIS EXACT JSON STRUCTURE:
{{
    "category_matches": true or false,
    "suggested_category": "string or null",
    "confidence_score": number between 0 and 1,
    "reason": "string or null"
}}
'''

SIMILARITY_CHECK_PROMPT = '''
Compare these two complaints and respond ONLY with a valid JSON object:

New Complaint:
Title: {title}
Description: {description}
Category: {category}

Existing Complaint:
Title: {existing_title}
Description: {existing_description}
Category: {existing_category}

Required JSON Response Format:
{{
    "is_similar": boolean,
    "similarity_score": float,
    "reason": string
}}
'''

def analyze_category(title, description, category, model):
    """Analyze complaint category with error handling and validation"""
    try:
        prompt = CATEGORY_ANALYSIS_PROMPT.format(title=title, description=description, category=category)

        response = model.generate_content([
            prompt
        ])
        
        
        try:
            analysis = json.loads(response.text)
        except json.JSONDecodeError:
            # If direct parsing fails, try cleaning the response
            cleaned_response = response.text.strip()
            cleaned_response = cleaned_response.replace('```json\n', '').replace('\n```', '')
            analysis = json.loads(cleaned_response)
        
        
        # Validate response structure
        required_fields = {'category_matches', 'suggested_category', 'confidence_score', 'reason'}
        if not all(field in analysis for field in required_fields):
            raise ValueError("Invalid response structure from model")
            
        return analysis
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from model: {str(e)}")
    except Exception as e:
        raise ValueError(f"Category analysis failed: {str(e)}")

def check_complaint_similarity(new_complaint, existing_complaints, model):
    """Check complaint similarity with improved error handling"""
    similar_complaints = []
    print('existing complaints')
    print(existing_complaints)
    
    for existing in existing_complaints:
        try:
            # Format prompt using the template placeholders
            prompt_content = SIMILARITY_CHECK_PROMPT.format(
                title=new_complaint['title'],
                description=new_complaint['description'],
                category=new_complaint['category'],
                existing_title=existing.title,
                existing_description=existing.description,
                existing_category=existing.category
            )
            
            response = model.generate_content([prompt_content])
            
            try:
                analysis = json.loads(response.text)
            except json.JSONDecodeError:
                # If direct parsing fails, try cleaning the response
                cleaned_response = response.text.strip()
                cleaned_response = cleaned_response.replace('```json\n', '').replace('\n```', '')
                analysis = json.loads(cleaned_response)
                print('analysis')
                print(analysis)
            
            # Validate and parse response
            required_fields = {'is_similar', 'similarity_score', 'reason'}
            if not all(field in analysis for field in required_fields):
                raise ValueError("Invalid response structure from model")
            
            if analysis.get('is_similar') and analysis.get('similarity_score', 0) > 0.6:
                # Use a new dict to store similarity data instead of modifying the model
                similar_complaint_data = {
                    'complaint': existing,
                    'similarity_score': analysis['similarity_score'],
                    'similarity_reason': analysis['reason']
                }
                similar_complaints.append(similar_complaint_data)
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response for complaint {existing.id}: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Error processing complaint {existing.id}: {str(e)}")
            continue
    
    print('similar complaints')
    print(similar_complaints)
    return similar_complaints

@api_view(['POST'])
def create_complaint(request, resident_id):
    try:
        # Common validation block - runs regardless of force_submit
        title = request.data.get('title')
        description = request.data.get('description')
        category = request.data.get('category')
        date = request.data.get('date')
        image = request.FILES.get('image')
        # If the value from flutter is 'true', then force_submit will be assigned True, else False
        force_submit = request.data.get('force_submit').lower() == 'true' 
        new_category = None

        # Validate required fields
        if not all([title, description, date, category]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate resident existence
        try:
            resident = Resident.objects.get(pk=resident_id)
        except Resident.DoesNotExist:
            return Response({'error': 'Resident not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Convert ISO 8601 datetime to date - should happen regardless of force_submit
        try:
            date = datetime.fromisoformat(date).date()
        except ValueError:
            return Response({'error': 'Invalid date format. Expected ISO 8601 format.'}, 
                        status=status.HTTP_400_BAD_REQUEST)

        # Image validation should happen regardless of force_submit
        if image:
            try:
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

                # Basic image integrity check
                with Image.open(image) as img:
                    img.verify()
                    image.seek(0)  # Reset file pointer after verify

            except (IOError, SyntaxError) as e:
                return Response({
                    'error': 'Invalid or corrupted image file'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Content analysis block - only runs if force_submit is False
        if not force_submit:
            # Text content analysis
            try:
                prompt = TEXT_ANALYSIS_PROMPT.format(
                    title=title,
                    description=description,
                )
                text_response = model.generate_content([prompt])
                

                text_analysis = json.loads(text_response.text)
                
                
                if text_analysis.get('has_inappropriate_content'):
                    return Response({
                        'error': 'The complaint contains inappropriate content'
                    }, status=status.HTTP_400_BAD_REQUEST)

                if not text_analysis.get('is_valid_complaint'):
                    return Response({
                        'error': 'The complaint appears to be invalid, spam or totally unrelated'
                    }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({
                    'error': f'Error analyzing complaint text: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Image content analysis
            if image:
                try:
                    img = Image.open(image)
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
                        
                except Exception as e:
                    return Response({
                        'error': f'Error processing image content: {str(e)}'
                    }, status=status.HTTP_400_BAD_REQUEST)

            #Category analysis
            try:
                category_analysis = analyze_category(title, description, category, model)
                

                if not category_analysis.get('category_matches') and category_analysis.get('confidence_score', 0) > 0.7:
                    new_category = category_analysis.get('suggested_category')
                    logger.info(f"Category changed from {category} to {new_category}")
            except Exception as e:
                return Response({
                    'error': ERROR_MESSAGES['category_analysis'].format(str(e))
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Similar complaints check
            try:
                ninety_days_ago = datetime.now().date() - timedelta(days=90)
                existing_complaints = Complaint.objects.filter(date__gte=ninety_days_ago)
                
                if existing_complaints.exists():
                    similar_complaints = check_complaint_similarity(
                        {
                            "title": title,
                            "description": description,
                            "category": category
                        },
                        existing_complaints,
                        model
                    )

                    if similar_complaints:
                        serialized_data = [
                            {
                                "title": item['complaint'].title,
                                "description": item['complaint'].description,
                                "category": item['complaint'].category,
                                "date": item['complaint'].date,
                                "similarity_score": item['similarity_score'],
                                "similarity_reason": item['similarity_reason']
                            }
                            for item in similar_complaints
                        ]

                        serializer = SimilarComplaintSerializer(
                            serialized_data,
                            many=True
                        )

                        return Response({
                            'warning': 'Similar complaints found',
                            'similar_complaints': serializer.data
                        }, status=status.HTTP_409_CONFLICT)
                        
            except Exception as e:
                return Response({
                    'error': ERROR_MESSAGES['similarity_check'].format(str(e))
                }, status=status.HTTP_400_BAD_REQUEST)

        # Create and save complaint - common block for both force_submit cases
        complaint = Complaint(
            resident=resident,
            title=title,
            description=description,
            date=date,
            category=new_category if new_category else category,
        )

        if image:
            complaint.image = image

        complaint.save()
        serializer = ComplaintSerializer(complaint)
        
        # Prepare response message based on category change
        response_data = serializer.data
        if new_category:
            response_data['message'] = f'Complaint created, category changed to {new_category}'
        else:
            response_data['message'] = 'Complaint created'

        return Response(
            response_data, 
            status=status.HTTP_201_CREATED if not force_submit else status.HTTP_200_OK
        )

    except Exception as e:
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