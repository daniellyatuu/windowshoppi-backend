from windowshoppi.api_permissions.permissions import IsExcAdminOrAdmin
from rest_framework.authentication import TokenAuthentication
from windowshoppi.pagination import StandardResultsSetPagination, MediumResultsSetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.master_data.models import Country
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer, UpdateAccountSerializer
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from app.user.models import User


class RegisterVendor(APIView):
    def post(self, request, format=None):
        data = self.request.data

        serializer = RegistrationSerializer(data=data)

        feedback = {}
        if serializer.is_valid():
            windowshoppi_user = serializer.save()

            # get user auth token
            token = Token.objects.get(user=windowshoppi_user)

            # get user phone numbers
            phone_number = windowshoppi_user.phone_numbers.all()[0]

            # get user business
            business = windowshoppi_user.user_business.all()[0]

            feedback['response'] = 'success'
            feedback['user_name'] = windowshoppi_user.username
            feedback['token'] = token.key
            feedback['business_id'] = business.id
            feedback['business_name'] = business.name
            feedback['business_location'] = business.location_name
            feedback['bio'] = business.bio
            feedback['call'] = phone_number.call
            feedback['whatsapp'] = phone_number.whatsapp
            feedback['profile_image'] = ''
            feedback['email'] = windowshoppi_user.email

            return Response(feedback, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsExcAdminOrAdmin]
    pagination_class = StandardResultsSetPagination


class ValidateUsername(APIView):
    def post(self, request, format=None):
        data = self.request.data

        username_res = {}
        username_res['user_exists'] = ''
        username_res['user_exists'] = User.objects.filter(
            username=data['username']).exists()
        return Response(username_res)


class UpdateBusinessInfo(APIView):
    serializer_class = UpdateAccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UpdateAccountSerializer(request.user, data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
