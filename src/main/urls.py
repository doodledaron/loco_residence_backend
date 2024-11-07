from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/residence/', include('residence.urls')),
    path('api/v1/finances/', include('finances.urls')),
    path('api/v1/announcements/', include('announcements.urls')),
    path('api/v1/bookings/', include('bookings.urls')),
    path('api/v1/visitors/', include('visitor.urls')),
    path('api/v1/complaints/', include('complaints.urls')),
    # Add this for serving media files in production
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)