import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from finances.serializers import CardSerializer, InvoiceSerializer
from users.models import Resident
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

#make payment
@api_view(['POST'])
def make_payment(request, resident_id):
    try:
        resident = Resident.objects.get(pk=resident_id)
        invoices = Invoice.objects.filter(resident=resident, status='unpaid')

        if not invoices.exists():
            return Response({'message': 'No unpaid invoices found for this resident'}, status=404)

        #get the total unpaid moount
        total_amount = sum([invoice.amount for invoice in invoices])

        # Assuming payment is successful
        for invoice in invoices:
            invoice.status = 'paid'
            invoice.save()

        return Response({'message': f'Payment of ${total_amount} made successfully for resident {resident_id}'}, status=200)

    except Resident.DoesNotExist:
        return Response({'message': 'Resident not found'}, status=404)

    except Exception as e:
        return Response({'message': str(e)}, status=500)


@api_view(['POST'])
def create_or_update_card(request, resident_id=None):
    try:
        # Check if the resident exists
        resident = Resident.objects.get(pk=resident_id)

        # Check if a card already exists for this resident
        cards = Card.objects.filter(resident=resident)

        # Prepare the card data from the request
        card_data = {
            'resident': resident.id,
            'card_no': request.data.get('card_no'),
            'card_type': request.data.get('card_type'),
            'card_expiry': request.data.get('card_expiry'),
            'card_cvv': request.data.get('card_cvv'),
            'card_name': request.data.get('card_name'),
            'card_status': 'active',
        }

        if cards.exists():
            # If a card exists, update the first card
            card = cards.first()
            serializer = CardSerializer(card, data=card_data)

            if serializer.is_valid():
                serializer.save()
                logger.info(f'Card updated successfully for resident {resident_id}')
                return Response(serializer.data, status=200)
            else:
                logger.error(f'Invalid data for card update: {serializer.errors}')
                return Response(serializer.errors, status=400)
        else:
            # If no card exists, create a new one
            serializer = CardSerializer(data=card_data)

            if serializer.is_valid():
                serializer.save()
                logger.info(f'Card created successfully for resident {resident_id}')
                return Response(serializer.data, status=201)
            else:
                logger.error(f'Invalid data for card creation: {serializer.errors}')
                return Response(serializer.errors, status=400)

    except Resident.DoesNotExist:
        logger.error(f'Resident not found with ID: {resident_id}')
        return Response({'message': 'Resident not found'}, status=404)


@api_view(['POST', 'DELETE'])
def delete_card(request, card_id):
    try:
        # Check if the method is POST or DELETE
        if request.method == 'DELETE':
            resident = Resident.objects.get(pk=1)

            card_to_delete = Card.objects.filter(
                pk=card_id,
                resident=resident
            )

            if not card_to_delete.exists():
                return Response({"error": "No card found to delete for the given parameters"}, status=404)

            deleted_card = card_to_delete.first()
            card_to_delete.delete()

            return Response({
                "message": "Card deleted successfully",
                "deleted_card": {
                    "id": deleted_card.id,
                    "card_no": deleted_card.card_no
                }
            }, status=status.HTTP_200_OK)

        # If method is POST, return an error (as it is not handled in this context)
        return Response({"error": "Invalid request method"}, status=405)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
