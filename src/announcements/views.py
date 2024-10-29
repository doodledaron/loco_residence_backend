from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Announcement
from .serializers import AnnouncementSerializer

@api_view(['GET'])
def view_all_announcements(request):
    try:
        announcements = Announcement.objects.filter(
            deleted_at__isnull=True
        ).order_by('-created_at')
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Announcement.DoesNotExist:
        return Response(
            {'error': 'No announcements found'}, 
            status=status.HTTP_404_NOT_FOUND
        )