from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.finances, name='finance-list-create'), #test url
    path('card/<int:resident_id>', views.get_card_by_resident, name='card-detail'), #get card by resident
    path('invoice/<int:resident_id>', views.get_invoice_by_resident, name='invoice-detail'), #get invoice by resident
    path('cards/create_update/<int:resident_id>/', views.create_or_update_card, name='create-update-card-details'),
    path('delete_card/<int:card_id>', views.delete_card),

]
