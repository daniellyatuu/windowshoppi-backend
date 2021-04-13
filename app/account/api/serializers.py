from django.shortcuts import get_object_or_404
from app.account.models import Account, Follow
from rest_framework import serializers
from rest_framework import status


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


class FollowAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']

    def create(self, validated_data):
        follower = self.validated_data['follower']
        following = self.validated_data['following']

        obj, created = Follow.objects.get_or_create(
            follower=follower, following=following)

        return created


class UnFollowAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']

    def create(self, validated_data):
        follower = self.validated_data['follower']
        following = self.validated_data['following']

        obj = get_object_or_404(Follow, follower=follower, following=following)
        obj.delete()  # delete object

        return 'deleted'
