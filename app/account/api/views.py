from windowshoppi.pagination import StandardResultsSetLimitOffset
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import AccountSerializer
from rest_framework.views import APIView
from app.account.models import Account
from django.db.models import Q


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
