from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import CreatePostSerializer, BussinessPostSerializer, PostImageSerializer
from app.user.models import User
from app.bussiness.models import Bussiness
from app.bussiness_post.models import BussinessPost, PostImage
from rest_framework.parsers import MultiPartParser, FormParser
from windowshoppi.api_permissions.permissions import IsAllowedToPost, IsBussinessBelongToMe


class CreatePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAllowedToPost, IsBussinessBelongToMe]
    parser_classes = (MultiPartParser, FormParser)


    def post(self, request, format=None):
        feedback = {}
        data = self.request.data

        images = dict((request.data))['filename']
        while("" in images):
            images.remove("")

        if len(images) == 0:
            feedback['error'] = 'image file is required'
            return Response(data=feedback, status=status.HTTP_400_BAD_REQUEST)

        if len(images) > 10:
            feedback['error'] = 'maximum file to upload is 10'
            return Response(data=feedback, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CreatePostSerializer(data=data)

        if serializer.is_valid():
            windowshoppi_post = serializer.save()
            
            feedback['response']='post created successfully'
            feedback['id']=windowshoppi_post.id
            
            return Response(feedback, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllPost(generics.ListAPIView):
    queryset = BussinessPost.objects.filter(active=True)
    serializer_class = BussinessPostSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


# class PostPhoto(generics.RetrieveAPIView):
#     queryset = PostImage.objects.all()
#     serializer_class = PostImageSerializer
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#     pagination_class = PageNumberPagination


class VendorPost(generics.ListAPIView):
    serializer_class = BussinessPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # get user active bussiness
        bussiness = Bussiness.objects.filter(user = self.request.user)[0]
        
        pk = bussiness.id
        return BussinessPost.objects.filter(bussiness__id=pk, active=True)
        
