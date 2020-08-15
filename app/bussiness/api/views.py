from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from app.bussiness.models import Bussiness
from .serializers import BussinessSerializer


class BusinessInfo(generics.RetrieveAPIView):
    queryset = Bussiness.objects.all()
    serializer_class = BussinessSerializer
