from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.finances, name='finance-list-create'), #test url
    path('card/<int:pk>', views.get_card_by_resident, name='card-detail'), #get card by resident
]
