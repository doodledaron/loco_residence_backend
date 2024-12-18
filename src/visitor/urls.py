from django.urls import path
from . import views


urlpatterns = [
    path('view_all_visitors/', views.view_all_visitors, name='view-all-visitors'), #list all visitors
    path('view_all_visitors/<int:resident_id>/',views.view_all_visitors, name='view_all_visitors_by_resident'),
    path('register_visitor/<int:resident_id>/', views.register_visitor, name='register-visitor'), #register a new visitor
    path('check_in_visitor/', views.check_in_visitor, name='check-in-visitor'), #list all visitors
    path('check_out_visitor/', views.check_out_visitor, name='check-out-visitor'), #check out a visitor
]
