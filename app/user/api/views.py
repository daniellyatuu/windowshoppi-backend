from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer, UpdateAccountSerializer, UpdateWindowshopperProfileSerializer, SwitchToBusinessAccountSerializer, UpdateVendorProfileSerializer, ChangePasswordSerializer, LoginSerializerOld
from windowshoppi.api_permissions.permissions import IsExcAdminOrAdmin, IsWindowshopperOrVendorAccount, IsAccountBelongToMe, IsContactBelongToMe
from windowshoppi.pagination import StandardResultsSetPagination, MediumResultsSetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework import status, generics
from app.master_data.models import Country
from rest_framework.views import APIView
from app.user.models import User, Contact
from app.account.models import Account
from django.urls import reverse


class RegisterUserView(APIView):

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, format=None):
        data = self.request.data

        serializer = self.serializer_class(data=data)

        feedback = {}
        if serializer.is_valid():
            result = serializer.save()

            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):  # will be removed

    permission_classes = [AllowAny]
    serializer_class = LoginSerializerOld

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserData(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWindowshopperOrVendorAccount]

    def get_object(self):
        obj = Account.objects.filter(
            user_id=self.request.user.id, selected=True).order_by('-date_modified')[0]
        return obj


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated, IsExcAdminOrAdmin]
#     pagination_class = StandardResultsSetPagination


class ValidateUsername(APIView):
    def post(self, request, format=None):
        data = self.request.data

        username_res = {}
        username_res['user_exists'] = ''
        username_res['user_exists'] = User.objects.filter(
            username=data['username']).exists()
        return Response(username_res)


class UpdateWhatsappNumber(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsContactBelongToMe]

    def get_queryset(self):
        data = get_object_or_404(Contact, pk=self.kwargs['contact_id'])
        return data

    def update(self, request, *args, **kwargs):

        # user instance
        user = request.user

        # get contact instance
        obj = self.get_queryset()

        # get user account
        account = user.user_account.filter(
            user=user, selected=True).order_by('-date_modified')[0]

        # update whatsapp number
        whatsapp = request.data.get('whatsapp')

        obj.whatsapp = whatsapp
        obj.save()

        result = {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'account_id': account.id,
            'account_name': account.name,
            'group': account.group.name,
            'profile_image': account.profile_image if account.profile_image else None,
            'account_bio': account.account_bio,
            'business_bio': account.business_bio,
            'location_name': account.location_name,
            'contact_id': obj.id,
            'call': obj.call,
            'whatsapp': obj.whatsapp,
            'date_registered': account.date_registered,
        }
        return Response(result)


class UpdateWindowshopperProfile(generics.UpdateAPIView):
    serializer_class = UpdateWindowshopperProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,
                          IsAccountBelongToMe, IsContactBelongToMe]

    def get_queryset(self, model, pk):
        data = get_object_or_404(model, pk=pk)
        return data

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():

            ########################################
            ''' update user '''
            ########################################

            # user instance
            user = request.user

            # get user data from form
            firstname = data.get('first_name')
            lastname = data.get('last_name')
            username = data.get('username')
            email = data.get('email')

            if user.username == username:
                ''' user dont want to change username '''

                user.first_name = firstname
                user.last_name = lastname
                user.email = email
                user.save()
            else:
                ''' user want to change username '''

                # make sure username dont exists to anyone except current user which is updating
                if User.objects.filter(username=username).exclude(username=user.username).exists():
                    result = {
                        'username': ['user with this username already exists.'],
                    }
                    return Response(result)
                else:
                    user.username = username
                    user.first_name = firstname
                    user.last_name = lastname
                    user.email = email
                    user.save()

            ########################################
            ''' update account '''
            ########################################

            # get account instance
            account = self.get_queryset(Account, self.kwargs['account_id'])

            # get account data from form
            account_bio = data.get('account_bio')

            account_name = user.first_name+' '+user.last_name

            account.name = account_name
            account.account_bio = account_bio
            account.save()

            ########################################
            ''' update contact '''
            ########################################

            # get contact instance
            contact = self.get_queryset(Contact, self.kwargs['contact_id'])

            # get contact data from form
            call = data.get('call')

            contact.call = call
            contact.save()

            result = {
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
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
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SwitchToBusinessAccount(generics.UpdateAPIView):
    serializer_class = SwitchToBusinessAccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,
                          IsAccountBelongToMe, IsContactBelongToMe]

    def get_queryset(self, model, pk):
        data = get_object_or_404(model, pk=pk)
        return data

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():

            ########################################
            ''' update user '''
            ########################################

            # user instance
            user = request.user

            # get user data from form
            username = data.get('username')
            email = data.get('email')

            if user.username == username:
                ''' user dont want to change username '''

                user.email = email
                user.save()
            else:
                ''' user want to change username '''

                # make sure username dont exists to anyone except current user which is updating
                if User.objects.filter(username=username).exclude(username=user.username).exists():
                    result = {
                        'username': ['user with this username already exists.'],
                    }
                    return Response(result)
                else:
                    user.username = username
                    user.email = email
                    user.save()

            ########################################
            ''' update account '''
            ########################################

            # get account instance
            account = self.get_queryset(Account, self.kwargs['account_id'])

            # get account data from form
            group_name = data.get('group')
            account_name = data.get('account_name')
            business_bio = data.get('business_bio')
            account_bio = data.get('account_bio')

            # get group instance
            group = get_object_or_404(Group, name=group_name)

            account.group = group
            account.name = account_name
            account.business_bio = business_bio
            account.account_bio = account_bio
            account.save()

            ########################################
            ''' update contact '''
            ########################################

            # get contact instance
            contact = self.get_queryset(Contact, self.kwargs['contact_id'])

            # get contact data from form
            call = data.get('call')
            whatsapp = data.get('whatsapp')

            contact.call = call
            contact.whatsapp = whatsapp
            contact.save()

            result = {
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
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
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateVendorProfile(generics.UpdateAPIView):
    serializer_class = UpdateVendorProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,
                          IsAccountBelongToMe, IsContactBelongToMe]

    def get_queryset(self, model, pk):
        data = get_object_or_404(model, pk=pk)
        return data

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():

            ########################################
            ''' update user '''
            ########################################

            # user instance
            user = request.user

            # get user data from form
            firstname = data.get('first_name')
            lastname = data.get('last_name')
            username = data.get('username')
            email = data.get('email')

            if user.username == username:
                ''' user dont want to change username '''

                user.first_name = firstname
                user.last_name = lastname
                user.email = email
                user.save()
            else:
                ''' user want to change username '''

                # make sure username dont exists to anyone except current user which is updating
                if User.objects.filter(username=username).exclude(username=user.username).exists():
                    result = {
                        'username': ['user with this username already exists.'],
                    }
                    return Response(result)
                else:
                    user.username = username
                    user.first_name = firstname
                    user.last_name = lastname
                    user.email = email
                    user.save()

            ########################################
            ''' update account '''
            ########################################

            # get account instance
            account = self.get_queryset(Account, self.kwargs['account_id'])

            # get account data from form
            account_name = data.get('account_name')
            business_bio = data.get('business_bio')
            account_bio = data.get('account_bio')

            account.name = account_name
            account.business_bio = business_bio
            account.account_bio = account_bio
            account.save()

            ########################################
            ''' update contact '''
            ########################################

            # get contact instance
            contact = self.get_queryset(Contact, self.kwargs['contact_id'])

            # get contact data from form
            call = data.get('call')
            whatsapp = data.get('whatsapp')

            contact.call = call
            contact.whatsapp = whatsapp
            contact.save()

            result = {
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
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
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):

        user = self.get_object()

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("current_password")):
                return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            ''' update token '''

            token = Token.objects.get(user=user)

            # delete existing token
            token.delete()

            # create new token
            new_token = Token.objects.create(user=user)

            response = {
                'token': new_token.key,
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
