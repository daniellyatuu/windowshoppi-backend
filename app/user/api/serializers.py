from rest_framework import serializers
from app.user.models import User, Contact
from app.bussiness.models import Bussiness
from app.master_data.models import Country, Category
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all())
    location_name = serializers.CharField(max_length=255)
    lattitude = serializers.FloatField()
    longitude = serializers.FloatField()
    call = serializers.CharField(max_length=17, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])

    class Meta:
        model = User
        fields = ['username', 'password', 'group', 'name', 'category',
                  'country', 'location_name', 'lattitude', 'longitude', 'call']
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
            username=username,
            group=group,
        )

        if len(password) < 4:
            raise serializers.ValidationError(
                {"password": "password too short"})
        windowshoppi_user.set_password(password)
        windowshoppi_user.save()

        # save contact
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


class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    call = serializers.CharField(max_length=255, read_only=True)
    whatsapp = serializers.CharField(max_length=255, read_only=True)
    business_id = serializers.IntegerField(read_only=True)
    business_name = serializers.CharField(max_length=255, read_only=True)
    business_location = serializers.CharField(max_length=255, read_only=True)
    bio = serializers.CharField(max_length=255, read_only=True)
    profile_image = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(max_length=255, read_only=True)

    def validate(self, data):

        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'username is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'invalid_account'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # get user token
        token = Token.objects.get(user=user).key

        # get user phone numbers
        phone_number = user.phone_numbers.all()[0]

        # get user bussiness
        bussiness = user.user_bussiness.all()[0]

        return {
            'token': token,
            'business_id': bussiness.id,
            'business_name': bussiness.name,
            'business_location': bussiness.location_name,
            'bio': bussiness.bio,
            'call': phone_number.call,
            'whatsapp': phone_number.whatsapp,
            'profile_image': bussiness.profile_image,
            'email': user.email,
        }


class BussinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bussiness
        fields = ['name', 'category', 'country',
                  'location_name', 'lattitude', 'longitude']


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


class UpdateAccountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    call = serializers.CharField(max_length=17, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    whatsapp = serializers.CharField(max_length=17, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    bio = serializers.CharField(max_length=5000, allow_blank=True)

    class Meta:
        model = User
        fields = ['name', 'call', 'whatsapp', 'email', 'bio']

    def update(self, instance, validated_data):
        business_name = self.validated_data['name']
        call_number = self.validated_data['call']
        whatsapp_number = self.validated_data['whatsapp']
        email_address = self.validated_data['email']
        bio = self.validated_data['bio']

        # update User Model
        instance.email = email_address
        instance.save()

        # update Contact Model

        formatedcallNumber = self.formatPhoneNumber(
            instance, call_number)

        formatedWhatsappNumber = self.formatPhoneNumber(
            instance, whatsapp_number)

        ''' get instance of User contact [0] '''
        phone_number = instance.phone_numbers.all()[0]
        phone_number.call = formatedcallNumber
        phone_number.whatsapp = formatedWhatsappNumber
        phone_number.save()

        # update Bussiness Model
        bussiness = instance.user_bussiness.all()[0]
        bussiness.name = business_name
        bussiness.bio = bio
        bussiness.save()

        # return instance
        return {
            'response': 'success',
            'name': bussiness.name,
            'call': phone_number.call,
            'whatsapp': phone_number.whatsapp,
            'email': instance.email,
            'bio': bussiness.bio,
        }

    def formatPhoneNumber(self, instance, phoneNumber):
        country_code = '255'
        number = phoneNumber[-9:]
        formatedNumber = country_code+number
        return formatedNumber
