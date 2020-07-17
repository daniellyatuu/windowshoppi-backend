from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import CountrySerializer
from app.master_data.models import Country
from rest_framework.parsers import MultiPartParser, FormParser


class AllCountry(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        country_list = Country.objects.filter(active=True)

        serializer = CountrySerializer(country_list, many=True)
        return Response(serializer.data)
