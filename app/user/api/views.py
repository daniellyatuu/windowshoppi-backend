from windowshoppi.api_permissions.permissions import IsExcAdminOrAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from app.master_data.models import Country, Category
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, UserSerializer
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
            token = Token.objects.get(user=windowshoppi_user).key
            
            feedback['response']='user registered successfully'
            feedback['id']=windowshoppi_user.id
            feedback['username']=windowshoppi_user.username
            feedback['token']=token
            
            return Response(feedback, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsExcAdminOrAdmin]
    pagination_class = PageNumberPagination