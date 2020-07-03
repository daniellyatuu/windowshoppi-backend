from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from app.user.models import User
from app.bussiness.models import Bussiness


class BussinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bussiness
        fields = ['name', 'category', 'location_name', 'lattitude', 'longitude']

        
class RegistrationSerializer(serializers.ModelSerializer):
    user_bussiness = BussinessSerializer(many=True)

    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password', 'email', 'country', 'group', 'user_bussiness']
        fields = ['username', 'password', 'confirm_password', 'email', 'country', 'group', 'user_bussiness']
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=['email']
        #     )
        # ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        bussiness_data = validated_data.pop('user_bussiness')
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"email": "user with this email already exists"})
        
        # save user
        windowshoppi_user = User(
            # first_name = self.validated_data['first_name'],
            # last_name = self.validated_data['last_name'],
            username = self.validated_data['username'],
            email = self.validated_data['email'].lower(),
            country = self.validated_data['country'],
            group = self.validated_data['group'],
        )

        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({"password": "password don't match"})
        if len(password) < 4:
            raise serializers.ValidationError({"password": "password too short"})
        windowshoppi_user.set_password(password)
        windowshoppi_user.save()

        # save user bussiness
        for data in bussiness_data:
            Bussiness.objects.create(user=windowshoppi_user, **data)
        return windowshoppi_user

    # def save(self):
    #     windowshoppi_user = User(
    #         first_name = self.validated_data['first_name'],
    #         last_name = self.validated_data['last_name'],
    #         username = self.validated_data['username'],
    #         email = self.validated_data['email'].lower(),
    #         country = self.validated_data['country'],
    #         group = self.validated_data['group'],
    #         )

    #     password = self.validated_data['password']
    #     confirm_password = self.validated_data['confirm_password']

    #     if password != confirm_password:
    #         raise serializers.ValidationError({"password": "password don't match"})
    #     if len(password) < 4:
    #         raise serializers.ValidationError({"password": "password too short"})
    #     windowshoppi_user.set_password(password)
    #     windowshoppi_user.save()
    #     return windowshoppi_user
        