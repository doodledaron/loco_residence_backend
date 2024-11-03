from complaints.models import Complaint
from rest_framework import serializers

class ComplaintSerializer(serializers.ModelSerializer):
    #image is not serialized since residents will no need to see others image
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'status', 'date']
        read_only_fields = ['status']


# Create a specialized serializer for similar complaints
class SimilarComplaintSerializer(serializers.ModelSerializer):
    # Fields from the Complaint model
    title = serializers.CharField()
    description = serializers.CharField()
    category = serializers.CharField()
    date = serializers.DateField()
    
    # Additional similarity data
    similarity_score = serializers.FloatField()
    similarity_reason = serializers.CharField()
    
    class Meta:
        model = Complaint
        fields = '__all__'