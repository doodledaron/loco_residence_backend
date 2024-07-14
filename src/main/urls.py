from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/residents/', include('residents.urls')),
    path('api/v1/residence/', include('residence.urls')),
    path('api/v1/finances/', include('finances.urls')),
    path('api/v1/announcements/', include('announcements.urls')),
]
