from rest_framework import serializers
from app.user.models import User, Contact
from app.bussiness.models import Bussiness


class BussinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bussiness
        fields = ['name', 'category', 'location_name', 'lattitude', 'longitude']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['call', 'whatsapp']

        
class RegistrationSerializer(serializers.ModelSerializer):
    user_bussiness = BussinessSerializer(many=True)
    phone_numbers = ContactSerializer(many=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'country', 'group', 'user_bussiness', 'phone_numbers']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        bussiness_data = validated_data.pop('user_bussiness')
        user_phone_number = validated_data.pop('phone_numbers')
        
        # save user
        windowshoppi_user = User(
            username = self.validated_data['username'],
            country = self.validated_data['country'],
            group = self.validated_data['group'],
        )

        password = self.validated_data['password']

        if len(password) < 4:
            raise serializers.ValidationError({"password": "password too short"})
        windowshoppi_user.set_password(password)
        windowshoppi_user.save()

        # save contact
        for phone_number in user_phone_number:
            Contact.objects.create(user=windowshoppi_user, **phone_number)

        # save user bussiness
        for data in bussiness_data:
            Bussiness.objects.create(user=windowshoppi_user, **data)
        return windowshoppi_user