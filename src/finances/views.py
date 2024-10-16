import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from finances.serializers import CardSerializer, InvoiceSerializer
from .models import Card, Invoice

# logger configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@api_view(['GET'])
def finances(request: Request) -> Response:
    logger.info('Finances view accessed')
    return Response({'message': 'Finances view accessed'})

@api_view(['GET'])
def get_card_by_resident(request, resident_id=None):
    try: 
        cards = Card.objects.filter(resident_id=resident_id)
        if cards.exists():
            serializer = CardSerializer(cards, many=True)
            return Response(serializer.data)
    except Card.DoesNotExist:
        return Response({'message': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_invoice_by_resident(request, resident_id=None):
    invoices = Invoice.objects.filter(resident_id=resident_id)
    if invoices.exists():
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_card_details(request, resident_id=None, card_id=None):
    try:
        # Get the card instance based on the resident ID and card ID
        card = Card.objects.get(resident_id=resident_id, id=card_id)

        # Deserialize the incoming data using CardSerializer
        serializer = CardSerializer(card, data=request.data)

        # Check if the incoming data is valid
        if serializer.is_valid():
            # Save the updated card details
            serializer.save()
            logger.info(f'Card {card_id} updated successfully for resident {resident_id}')
            return Response(serializer.data)
        else:
            logger.error(f'Invalid data for card update: {serializer.errors}')
            return Response(serializer.errors, status=400)
    
    except Card.DoesNotExist:
        logger.error(f'Card not found for resident {resident_id} and card {card_id}')
        return Response({'message': 'Card not found'}, status=404)
