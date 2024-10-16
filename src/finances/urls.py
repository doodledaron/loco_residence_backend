from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.finances, name='finance-list-create'), #test url
    path('card/<int:resident_id>', views.get_card_by_resident, name='card-detail'), #get card by resident
    path('invoice/<int:resident_id>', views.get_invoice_by_resident, name='invoice-detail'), #get invoice by resident
    path('cards/update/<int:resident_id>/<int:card_id>/', views.update_card_details, name='update-card-details'),

]
