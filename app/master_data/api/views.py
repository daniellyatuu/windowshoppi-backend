from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CountrySerializer, HashTagSerializer
from rest_framework.authentication import TokenAuthentication
from windowshoppi.pagination import LargeResultsSetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from app.master_data.models import Country, HashTag
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView


class CreateCountry(generics.CreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class AllCountry(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class Top30HashTags(APIView):
    def get(self, request):
        category_list = HashTag.objects.raw(
            'SELECT id, name FROM master_data_hashtag ORDER BY visited DESC LIMIT 30')

        serializer = HashTagSerializer(category_list, many=True)
        return Response(serializer.data)


class HashTagList(generics.ListAPIView):
    serializer_class = HashTagSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = HashTag.objects.filter(
            active=True).order_by('id')
        return queryset
