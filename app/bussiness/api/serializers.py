from rest_framework import serializers
from app.bussiness.models import Bussiness


class BussinessSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    call_number = serializers.CharField(source='user.call_phone_number')
    whatsapp_number = serializers.CharField(
        source='user.whatsapp_phone_number')

    class Meta:
        model = Bussiness
        fields = ['name', 'profile_image', 'bio', 'location_name',
                  'email', 'call_number', 'whatsapp_number']
