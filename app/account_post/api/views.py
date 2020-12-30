from rest_framework.authentication import TokenAuthentication
from windowshoppi.pagination import StandardResultsSetLimitOffset, MediumResultsSetPagination
from .serializers import CreatePostSerializer, AccountPostSerializer, CreatePostSerializerOld, UpdatePostSerializer, BussinessPostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from app.account.models import Account
from app.account_post.models import AccountPost
from rest_framework.parsers import MultiPartParser, FormParser
from windowshoppi.api_permissions.permissions import IsWindowshopperOrVendorAccount, IsAccountBelongToMe
from django.utils import timezone
from datetime import timedelta
from itertools import chain
import random


class CreatePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,
                          IsWindowshopperOrVendorAccount, IsAccountBelongToMe]
    # permission_classes = [IsAuthenticated,
    #                       IsAllowedToPost, IsBussinessBelongToMe]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = CreatePostSerializer

    def post(self, request, format=None):

        data = self.request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            result = serializer.save()

            if(result == 'error_occurred'):
                return Response(result, status=status.HTTP_501_NOT_IMPLEMENTED)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleUserAccountPostView(generics.RetrieveAPIView):
    queryset = AccountPost.objects.all()
    serializer_class = AccountPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CreatePostViewOld(APIView):  # will be removed
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsWindowshopperOrVendorAccount]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = CreatePostSerializerOld

    def post(self, request, format=None):

        data = self.request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            result = serializer.save()
            if result:
                feedback = {}
                feedback = 'success'
                return Response(feedback, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountPostView(generics.ListAPIView):
    serializer_class = AccountPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetLimitOffset

    def get_queryset(self):

        if self.kwargs:
            account_id = self.kwargs['pk']
        else:
            account = Account.objects.filter(user=self.request.user)[0]
            account_id = account.id

        return AccountPost.objects.filter(account_id=account_id, active=True)


class SearchPost(generics.ListAPIView):
    serializer_class = AccountPostSerializer
    pagination_class = StandardResultsSetLimitOffset

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        if(keyword != ''):
            queryset = AccountPost.objects.filter(
                active=True, caption__icontains=keyword)
            return queryset
        else:
            raise ValidationError(
                detail="keyword is required")


class SearchPostOld(generics.ListAPIView):  # will be removed
    serializer_class = AccountPostSerializer
    pagination_class = MediumResultsSetPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        if(keyword != ''):
            queryset = AccountPost.objects.filter(
                active=True, caption__icontains=keyword)
            return queryset
        else:
            raise ValidationError(
                detail="keyword is required")


class UpdatePost(generics.RetrieveUpdateAPIView):
    queryset = AccountPost.objects.all()
    serializer_class = UpdatePostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class BusinessPost(generics.ListAPIView):  # will be removed
    serializer_class = BussinessPostSerializer
    pagination_class = MediumResultsSetPagination

    def get_queryset(self):
        id = self.kwargs['pk']
        return AccountPost.objects.filter(account_id=id, active=True)


class AccountPostView(generics.ListAPIView):
    serializer_class = AccountPostSerializer
    pagination_class = StandardResultsSetLimitOffset

    def get_queryset(self):
        id = self.kwargs['pk']
        return AccountPost.objects.filter(account_id=id, active=True)


class AllPost(generics.ListAPIView):  # will be removed

    serializer_class = BussinessPostSerializer
    pagination_class = MediumResultsSetPagination

    def get_queryset(self):

        return AccountPost.objects.filter(active=True)


class AccountPostListView(generics.ListAPIView):

    serializer_class = AccountPostSerializer
    pagination_class = StandardResultsSetLimitOffset

    def get_queryset(self):
        current_time = timezone.now()
        time_diff = timedelta(minutes=40)
        time_range = current_time - time_diff

        # queryset1 = AccountPost.objects.filter(
        #     active=True, date_posted__gte=time_range)

        queryset2 = AccountPost.objects.filter(
            active=True).order_by('?')

        # result_queryset = list(chain(queryset1, queryset2))

        return queryset2
