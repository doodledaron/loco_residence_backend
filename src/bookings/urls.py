from django.urls import path
from . import views

urlpatterns = [
    path('facility_types/', views.get_facility_types),
    path('facilities/', views.get_facilities),
    path('available_slots/<int:facility_id>/<str:date>/', views.get_available_slots),
    # path('book_facility/', views.book_facility),
    path('user_bookings/', views.get_user_bookings),
    # path('cancel_booking/', views.cancel_booking),
]