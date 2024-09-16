from django.urls import path
from . import views

urlpatterns = [
    path('facilities/', views.get_facilities),
    path('available_time_slots/', views.get_available_time_slots),
    # path('book_facility/', views.book_facility),
    path('available_facility_sections/', views.get_available_facility_sections),
    path('book_facility_section/', views.book_facility_section),
    path('cancel_booking/', views.cancel_booking),
    # path('cancel_booking/', views.cancel_booking),
]