from django.urls import path
from . import views


urlpatterns = [
    path('create_complaint/<int:resident_id>/', views.create_complaint, name='create-complaint'), #create a complaint
    path('view_all_complaints/<int:resident_id>/', views.view_all_complaints, name='view-all-complaints'), #list all complaints
]
