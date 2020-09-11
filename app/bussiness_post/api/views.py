from rest_framework.authentication import TokenAuthentication
from windowshoppi.pagination import StandardResultsSetPagination, MediumResultsSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import CreatePostSerializer, BussinessPostSerializer, PostImageSerializer, UpdatePostSerializer
from app.user.models import User
from app.bussiness.models import Bussiness
from app.bussiness_post.models import BussinessPost, PostImage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from windowshoppi.api_permissions.permissions import IsAllowedToPost, IsBussinessBelongToMe
from PIL import Image, ImageDraw, ImageFont


class CreatePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,
                          IsAllowedToPost, IsBussinessBelongToMe]
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
            feedback = 'success'
            return Response(feedback, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllPost(generics.ListAPIView):

    serializer_class = BussinessPostSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = MediumResultsSetPagination
    # changed here

    def get_queryset(self):
        countryid = self.request.GET.get('country', '')
        categoryid = self.request.GET.get('category', '')
        print(countryid)
        print(categoryid)
        category = int(categoryid)

        if(category == 0):
            queryset = BussinessPost.objects.filter(
                active=True, bussiness__country_id=countryid)
        else:
            queryset = BussinessPost.objects.filter(
                active=True, bussiness__country_id=countryid, bussiness__category_id=categoryid)

        return queryset


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
    pagination_class = MediumResultsSetPagination

    def get_queryset(self):
        # git pull is working fine
        bussiness = Bussiness.objects.filter(user=self.request.user)[0]

        pk = bussiness.id
        return BussinessPost.objects.filter(bussiness_id=pk, active=True)


class BusinessPost(generics.ListAPIView):
    serializer_class = BussinessPostSerializer
    pagination_class = MediumResultsSetPagination

    def get_queryset(self):

        id = self.kwargs['pk']
        return BussinessPost.objects.filter(bussiness_id=id, active=True)


class SearchPost(generics.ListAPIView):
    serializer_class = BussinessPostSerializer
    pagination_class = MediumResultsSetPagination

    def get_queryset(self):
        countryid = self.request.query_params.get('country', '')
        keyword = self.request.query_params.get('keyword', '')

        if(keyword != ''):
            queryset = BussinessPost.objects.filter(
                active=True, caption__icontains=keyword, bussiness__country_id=countryid)
            return queryset
        else:
            raise ValidationError(
                detail="keyword is required")


class SearchPostByCategory(generics.ListAPIView):
    serializer_class = BussinessPostSerializer

    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        countryid = self.request.query_params.get('country', '')
        categoryid = self.kwargs['pk']

        categoryid = int(categoryid)

        queryset = BussinessPost.objects.filter(
            active=True, bussiness__category_id=categoryid, bussiness__country_id=countryid)
        return queryset


# class InsertTextToImage(APIView):
#     def get(self, request, format=None):
#         image = Image.open('media/post_pics/image_1_1596722055119.jpg')
#         draw = ImageDraw.Draw(image)
#         points = 100, 100
#         string = "from windowshoppi.com"
#         font1 = ImageFont.truetype('arial.ttf', 50)
#         draw.text(points, string, 'white', font=font1)

#         print(image)
#         image.show()
#         return Response('start inserting')


class UpdatePost(generics.RetrieveUpdateAPIView):
    queryset = BussinessPost.objects.all()
    serializer_class = UpdatePostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
