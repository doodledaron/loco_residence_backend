import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from finances.serializers import CardSerializer
from .models import Card

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
def get_card_by_resident(request, pk=None):
    try: 
        card = Card.objects.get(id=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)
    except Card.DoesNotExist:
        return Response({'message': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
