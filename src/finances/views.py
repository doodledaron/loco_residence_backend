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
    try:
        invoices = Invoice.objects.filter(resident_id=resident_id)
        if invoices.exists:
            serializer = InvoiceSerializer(invoices, many=True)
            return Response(serializer.data)
    except Invoice.DoesNotExist:
        return Response({'message': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)