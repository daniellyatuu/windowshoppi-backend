from app.user.user_background_tasks import notify_user
from rest_framework.validators import UniqueValidator
from app.master_data.models import Country, HashTag
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from windowshoppi.settings.base import MEDIA_URL
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from app.bussiness.models import Bussiness
from app.user.models import User, Contact
from rest_framework import serializers
from app.account.models import Account
from django.utils import timezone


class RegistrationSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(), slug_field='name')
    call = serializers.CharField(max_length=17, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    call_iso_code = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password', 'group', 'call', 'call_iso_code']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        firstname = self.validated_data.get('first_name', None)
        lastname = self.validated_data.get('last_name', None)
        username = self.validated_data['username']
        email_address = self.validated_data.get('email', None)
        password = self.validated_data['password']
        group = self.validated_data.get('group', None)
        call = self.validated_data['call']
        call_iso_code = self.validated_data.get('call_iso_code')

        # validation
        if firstname == None:
            raise serializers.ValidationError(
                {'first_name': ['This field is required.']})

        if lastname == None:
            raise serializers.ValidationError(
                {'last_name': ['This field is required.']})

        if len(password) < 4:
            raise serializers.ValidationError(
                {"password": ["password too short"]})

        if group == None:
            raise serializers.ValidationError(
                {'group': ['This field is required.']})

        # save user
        windowshoppi_user = User(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email_address,
        )

        windowshoppi_user.set_password(password)
        windowshoppi_user.save()

        # save account data
        account_name = firstname+' '+lastname
        account = Account.objects.create(
            name=account_name, user=windowshoppi_user, group=group)

        # save contact
        contact = Contact.objects.create(
            user=windowshoppi_user, call=call, call_iso_code=call_iso_code)

        # # notify user
        # notify_user(windowshoppi_user.id, schedule=timezone.now())

        # get user auth token
        token = Token.objects.get(user=windowshoppi_user).key

        return {
            'token': token,
            'user_id': windowshoppi_user.id,
            'username': windowshoppi_user.username,
            'first_name': windowshoppi_user.first_name,
            'last_name': windowshoppi_user.last_name,
            'email': windowshoppi_user.email,
            'account_id': account.id,
            'account_name': account.name,
            'group': account.group.name,
            'profile_image': account.profile_image if account.profile_image else None,
            'account_bio': account.account_bio,
            'business_bio': account.business_bio,
            'location_name': account.location_name,
            'contact_id': contact.id,
            'call': contact.call,
            'whatsapp': contact.whatsapp,
            'date_registered': account.date_registered,
        }


class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """

    # fields for user login
    user_name = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # fields to return user data after login
    token = serializers.CharField(max_length=255, read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    account_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(max_length=255, read_only=True)
    account_name = serializers.CharField(max_length=255, read_only=True)
    group = serializers.CharField(max_length=255, read_only=True)
    profile_image = serializers.ImageField(read_only=True)
    account_bio = serializers.CharField(max_length=500, read_only=True)
    business_bio = serializers.CharField(max_length=255, read_only=True)
    location_name = serializers.CharField(max_length=255, read_only=True)
    contact_id = serializers.IntegerField(read_only=True)
    call = serializers.CharField(max_length=255, read_only=True)
    whatsapp = serializers.CharField(max_length=255, read_only=True)

    # will be removed later on
    result = serializers.CharField(max_length=10, read_only=True)

    def validate(self, data):

        user_name = data.get('user_name', None)
        password = data.get('password', None)

        user = authenticate(username=user_name, password=password)

        if user is None:
            raise serializers.ValidationError('invalid_account')

        # get user account
        user_account = user.user_account.all()

        # make sure logged in user is windowshopper or vendor
        allowed_groups = ['windowshopper', 'vendor']

        user_groups = []
        for account in user_account:
            user_groups.append(account.group.name)

        result = any(group in user_groups for group in allowed_groups)

        if result:

            # save user last_login
            user.last_login = timezone.now()
            user.save()

            # get selected user account
            selected_account = user_account.filter(
                user_id=user.id, selected=True).order_by('-date_modified')[0]

            # get user token
            token = Token.objects.get(user=user).key

            # get user phone numbers
            phone_number = user.phone_numbers.all()[0]

            if account.profile_image:
                profile_image = MEDIA_URL + str(account.profile_image)
            else:
                profile_image = None

            return {
                'result': 'success',  # will be removed

                'token': token,
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'account_id': account.id,
                'account_name': account.name,
                'group': account.group,
                'profile_image': account.profile_image,
                'account_bio': account.account_bio,
                'business_bio': account.business_bio,
                'location_name': account.location_name,
                'contact_id': phone_number.id,
                'call': phone_number.call,
                'whatsapp': phone_number.whatsapp,
                'date_registered': account.date_registered,
            }
        else:
            return {
                'result': 'access_to_vendor_only'
            }


class LoginSerializerOld(serializers.Serializer):  # will be removed
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
        bussiness = user.user_account.all()[0]

        if bussiness.profile_image:
            profile_image = MEDIA_URL + str(bussiness.profile_image)
        else:
            profile_image = None

        return {
            'token': token,
            'business_id': bussiness.id,
            'business_name': bussiness.name,
            'business_location': bussiness.location_name,
            'bio': bussiness.account_bio,
            'call': phone_number.call,
            'whatsapp': phone_number.whatsapp,
            'profile_image': bussiness.profile_image,
            'email': user.email,
        }


class UserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    account_id = serializers.IntegerField(source='id')
    account_name = serializers.CharField(source='name')
    contact_id = serializers.IntegerField(source='user.contact_id')
    call = serializers.CharField(source='user.call_phone_number')
    call_iso_code = serializers.CharField(source='user.call_iso_code')
    whatsapp_iso_code = serializers.CharField(source='user.whatsapp_iso_code')
    whatsapp = serializers.CharField(source='user.whatsapp_phone_number')

    class Meta:
        model = Account
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'account_id', 'account_name', 'group',
                  'profile_image', 'account_bio', 'business_bio', 'location_name', 'contact_id', 'call', 'call_iso_code', 'whatsapp', 'whatsapp_iso_code', 'date_registered']


# class UserSerializer(serializers.ModelSerializer):
#     user_account = AccountSerializer(many=True)
#     phone_numbers = ContactSerializer(many=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name',
#                   'email', 'date_joined', 'user_account', 'phone_numbers']


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

        print(phone_number)
        # update Bussiness Model
        bussiness = instance.user_account.all()[0]

        bussiness.name = business_name
        bussiness.account_bio = bio
        bussiness.save()

        # return instance
        return {
            'response': 'success',
            'name': bussiness.name,
            'call': phone_number.call,
            'whatsapp': phone_number.whatsapp,
            'email': instance.email,
            'bio': bussiness.account_bio,
        }

    def formatPhoneNumber(self, instance, phoneNumber):
        country_code = '255'
        number = phoneNumber[-9:]
        formatedNumber = country_code+number
        return formatedNumber


class UpdateWindowshopperProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    call = serializers.CharField(max_length=17, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    account_bio = serializers.CharField(
        max_length=5000, allow_blank=True, required=False)
    email = serializers.EmailField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'call', 'account_bio', 'email']


class UpdateVendorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    account_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    business_bio = serializers.CharField(max_length=30)
    call = serializers.CharField(max_length=17, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    whatsapp = serializers.CharField(max_length=17, required=False, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    account_bio = serializers.CharField(
        max_length=5000, allow_blank=True, required=False)
    email = serializers.EmailField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'account_name', 'username',
                  'business_bio', 'call', 'whatsapp', 'account_bio', 'email']


class SwitchToBusinessAccountSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(), slug_field='name')
    account_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    business_bio = serializers.CharField(max_length=30)
    call = serializers.CharField(max_length=17, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    whatsapp = serializers.CharField(max_length=17, required=False, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    account_bio = serializers.CharField(
        max_length=5000, allow_blank=True, required=False)
    email = serializers.EmailField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['group', 'account_name', 'username',
                  'business_bio', 'call', 'whatsapp', 'account_bio', 'email']


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=4, required=True)

# class UpdateWhatsappNumberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ['whatsapp']
