from django.urls import path
from . import views

urlpatterns = [
    path('view_all_announcements/', views.view_all_announcements, name='view-all-announcements'),
]