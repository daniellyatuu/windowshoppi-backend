from rest_framework import serializers
from app.user.models import User, Contact
from app.bussiness.models import Bussiness
from app.master_data.models import Country, Category
from django.core.validators import RegexValidator

        
class RegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    location_name = serializers.CharField(max_length=255)
    lattitude = serializers.FloatField()
    longitude = serializers.FloatField()
    call = serializers.CharField(max_length=17, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])

    class Meta:
        model = User
        fields = ['username', 'password', 'group', 'name', 'category', 'country', 'location_name', 'lattitude', 'longitude', 'call']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = self.validated_data['username']
        password = self.validated_data['password']
        group = self.validated_data['group']
        name = self.validated_data['name']
        category = self.validated_data['category']
        country = self.validated_data['country']
        location_name = self.validated_data['location_name']
        lattitude = self.validated_data['lattitude']
        longitude = self.validated_data['longitude']
        call = self.validated_data['call']
        
        # save user
        windowshoppi_user = User(
            username = username,
            group = group,
        )

        if len(password) < 4:
            raise serializers.ValidationError({"password": "password too short"})
        windowshoppi_user.set_password(password)
        windowshoppi_user.save()

        # save contact
        # for phone_number in user_phone_number:
        Contact.objects.create(
            user=windowshoppi_user, call=call,
        )

        # save user bussiness
        Bussiness.objects.create(
            user=windowshoppi_user,
            name=name,
            category=category,
            country=country,
            location_name=location_name,
            lattitude=lattitude,
            longitude=longitude,
        )
        return windowshoppi_user


class BussinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bussiness
        fields = ['name', 'category', 'country', 'location_name', 'lattitude', 'longitude']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['call', 'whatsapp']

        
class UserSerializer(serializers.ModelSerializer):
    user_bussiness = BussinessSerializer(many=True)
    phone_numbers = ContactSerializer(many=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'group', 'user_bussiness', 'phone_numbers']
