from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from app.user.models import User
from django.contrib.auth.models import Group
from .serializers import RegistrationSerializer
from app.master_data.models import Country, Category
from rest_framework.authtoken.models import Token


class RegisterUser(APIView):
    def post(self, request, format=None):
        data = self.request.data
        
        serializer = RegistrationSerializer(data=data)
        
        feedback = {}
        if serializer.is_valid():
            windowshoppi_user = serializer.save()
            token = Token.objects.get(user=windowshoppi_user).key
            
            feedback['response']='user registered successfully'
            feedback['username']=windowshoppi_user.username
            feedback['email']=windowshoppi_user.email
            feedback['token']=token
            
            return Response(feedback, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)