from django.urls import path
from . import views

urlpatterns = [
    path('facilities/', views.get_facilities),
    path('available_time_slots/', views.get_available_time_slots),
    path('available_facility_sections/', views.get_available_facility_sections),
    path('book_facility_section/<int:resident_id>/', views.book_facility_section),
    path('cancel_booking/<int:resident_id>/', views.cancel_booking),
    path('get_all_bookings/<int:resident_id>/', views.get_all_bookings),
]