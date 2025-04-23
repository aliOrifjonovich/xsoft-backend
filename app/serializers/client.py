from rest_framework import serializers
from app.models.client import Client

class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'fullname', 'email', 'phone_number', 'address', 
            'passportid', 'driverLicense', 'licenseExpiry', 
            'age', 'status'
        ] 
class CleintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
