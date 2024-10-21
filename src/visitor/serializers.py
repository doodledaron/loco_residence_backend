from visitor.models import Visitor
from rest_framework import serializers

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = [
            'id','resident', 'full_name', 'hp_number', 'car_plate_no',
            'check_in_date', 'check_out_date', 'check_in_time', 
            'check_out_time', 'purpose_of_visit'
        ]
        read_only_fields = ['resident']
