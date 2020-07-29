from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from windowshoppi.pagination import LargeResultsSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import CountrySerializer, CategorySerializer
from app.master_data.models import Country, Category
from rest_framework.parsers import MultiPartParser, FormParser


class CreateCountry(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        data = self.request.data

        serializer = CountrySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllCountry(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        country_list = Country.objects.filter(active=True)

        serializer = CountrySerializer(country_list, many=True)
        return Response(serializer.data)


class Top30Category(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        category_list = Category.objects.raw(
            'SELECT id, name FROM master_data_category ORDER BY visited DESC LIMIT 30')

        serializer = CategorySerializer(category_list, many=True)
        return Response(serializer.data)


class AllCategory(generics.ListAPIView):

    serializer_class = CategorySerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = Category.objects.filter(
            active=True).order_by('id')
        return queryset
