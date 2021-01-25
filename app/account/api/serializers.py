from rest_framework import serializers
from app.account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    account_id = serializers.IntegerField(source='id')
    account_name = serializers.CharField(source='name')
    username = serializers.CharField(source='user.username')
    group = serializers.CharField(source='group.name')
    email = serializers.CharField(source='user.email')
    call_number = serializers.CharField(source='user.call_phone_number')
    call_dial_code = serializers.CharField(source='user.call_dial_code')
    whatsapp_number = serializers.CharField(
        source='user.whatsapp_phone_number')
    whatsapp_dial_code = serializers.CharField(
        source='user.whatsapp_dial_code')

    class Meta:
        model = Account
        fields = ['account_id', 'account_name', 'username', 'group', 'email',
                  'call_number', 'call_dial_code', 'whatsapp_number', 'whatsapp_dial_code', 'profile_image', 'account_bio', 'business_bio']
