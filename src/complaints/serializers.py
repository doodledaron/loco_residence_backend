from complaints.models import Complaint
from rest_framework import serializers

class ComplaintSerializer(serializers.ModelSerializer):
    #image is not serialized since residents will no need to see others image
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'status', 'date']
        read_only_fields = ['status']