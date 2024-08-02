from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        #prevent it from being exposed in responses.
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        #create a user with the validated data
        user = CustomUser.objects.create_user(**validated_data)
        return user