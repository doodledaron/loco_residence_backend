from django.urls import path
from . import views

urlpatterns = [
    path('facilities/', views.get_facilities),
    path('available_slots/', views.get_available_slots),
    # path('book_facility/', views.book_facility),
    path('user_bookings/', views.get_user_bookings),
    path('create_booking/', views.create_booking),
    # path('cancel_booking/', views.cancel_booking),
]