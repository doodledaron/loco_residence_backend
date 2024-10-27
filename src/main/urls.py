from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/residence/', include('residence.urls')),
    path('api/v1/finances/', include('finances.urls')),
    path('api/v1/announcements/', include('announcements.urls')),
    path('api/v1/bookings/', include('bookings.urls')),
    path('api/v1/visitors/', include('visitor.urls')),
    path('api/v1/complaints/', include('complaints.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
