from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/residents/', include('residents.url')),
    path('api/v1/residence/', include('residence.url')),
    path('api/v1/finances/', include('finances.url')),
    path('api/v1/announcements/', include('announcements.url')),
]
