from windowshoppi.api_permissions.permissions import IsAccountBelongToMe, IsContactBelongToMe
from windowshoppi.pagination import StandardResultsSetLimitOffset
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from windowshoppi.settings.base import MEDIA_URL
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import AccountSerializer
from rest_framework.views import APIView
from app.account.models import Account
from resizeimage import resizeimage
from app.user.models import Contact
from django.core.files import File
from django.db.models import Q
from datetime import datetime
from io import BytesIO
from PIL import Image
import os


class AccountDetail(generics.RetrieveAPIView):
    queryset = Account.objects.filter(active=True)
    serializer_class = AccountSerializer


class SearchAccount(generics.ListAPIView):
    serializer_class = AccountSerializer
    pagination_class = StandardResultsSetLimitOffset

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')

        if(keyword != ''):
            queryset = Account.objects.filter(
                Q(active=True), Q(name__icontains=keyword) | Q(user__username__icontains=keyword))
            return queryset
        else:
            raise ValidationError(
                detail="keyword is required")


class UpdateUserProfilePictureView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAccountBelongToMe]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        data = get_object_or_404(Account, pk=self.kwargs['account_id'])
        return data

    def post(self, request, *args, **kwargs):

        data = self.request.data

        # user instance
        user = request.user

        # get account instance
        account = self.get_queryset()

        feedback = {}

        if 'profile_picture' not in data:
            feedback['error'] = 'profile_picture is required'
            return Response(data=feedback, status=status.HTTP_400_BAD_REQUEST)

        image = dict((request.data))['profile_picture']

        while("" in image):
            image.remove("")

        if len(image) == 0:
            feedback['error'] = 'profile_picture must not be empty'
            return Response(data=feedback, status=status.HTTP_400_BAD_REQUEST)

        if len(image) > 1:
            feedback['error'] = 'maximum file to upload is 1'
            return Response(data=feedback, status=status.HTTP_400_BAD_REQUEST)

        # get filename
        picture = ''
        for filename in image:
            picture = filename

        #########################
        # compress image .start
        #########################

        im = Image.open(picture)

        im = im.convert('RGB')

        # get filename extension
        name, ext = os.path.splitext(filename.name)

        ''' new filename '''
        # current date and time
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        new_name = name + str(timestamp)
        new_name = new_name.replace('.', '')

        new_filename = new_name+ext

        max_width = 720
        if im.size[0] > max_width:
            im = resizeimage.resize_width(im, max_width)
        im_io = BytesIO()

        im.save(im_io, 'JPEG', quality=60)
        new_image = File(im_io, name=new_filename)

        #########################
        # compress image .end
        #########################

        # update profile picture
        try:
            account.profile_image = new_image
            account.save()

            result = {
                'user_id': user.id,
            }
            return Response(result)

        except:
            feedback['error'] = 'failed to upload image to storage'
            return Response(data=feedback, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveProfilePictureView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,
                          IsAccountBelongToMe, IsContactBelongToMe]

    def get_queryset(self, model, pk):
        data = get_object_or_404(model, pk=pk)
        return data

    def put(self, request, *args, **kwargs):

        # user instance
        user = request.user

        # get account instance
        account = self.get_queryset(Account, self.kwargs['account_id'])

        # get contact instance
        contact = self.get_queryset(Contact, self.kwargs['contact_id'])

        # remove profile picture
        account.profile_image = None
        account.save()

        if account.profile_image:
            profile_image = MEDIA_URL + str(account.profile_image)
        else:
            profile_image = None

        result = {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'account_id': account.id,
            'account_name': account.name,
            'group': account.group.name,
            'profile_image': profile_image,
            'account_bio': account.account_bio,
            'business_bio': account.business_bio,
            'location_name': account.location_name,
            'contact_id': contact.id,
            'call': contact.call,
            'whatsapp': contact.whatsapp,
            'date_registered': account.date_registered,
        }
        return Response(result)
