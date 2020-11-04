from rest_framework import serializers
from app.bussiness_post.models import BussinessPost, PostImage


class CreatePostSerializer(serializers.ModelSerializer):
    filename = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False))

    class Meta:
        model = BussinessPost
        fields = ['bussiness', 'caption', 'filename']

    def create(self, validated_data):
        bussiness = self.validated_data['bussiness']
        caption = self.validated_data['caption']
        filename = validated_data.pop('filename')

        # save post
        windowshoppi_post = BussinessPost.objects.create(
            bussiness=bussiness,
            caption=caption,
        )

        # save post images
        # image_list = []
        # for image in filename:
        #     # resizedImage = self.compress(image)
        #     image_list.append(
        #         PostImage(post=windowshoppi_post, filename=image))
        # PostImage.objects.bulk_create(image_list)

        for image in filename:
            PostImage.objects.create(post=windowshoppi_post, filename=image)

        return windowshoppi_post

    # def compress(self, filename):
    #     im = Image.open(filename)
    #     im_io = BytesIO()
    #     # im.save(im_io, 'JPEG', quality=60)
    #     # new_image = File(im_io, name=filename.name)
    #     # return new_image


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['filename']


class BussinessPostSerializer(serializers.ModelSerializer):
    post_photos = PostImageSerializer(many=True)
    user_name = serializers.CharField(source='bussiness.user')
    account_name = serializers.CharField(source='bussiness.name')
    business_location = serializers.CharField(source='bussiness.location_name')
    account_profile = serializers.CharField(source='bussiness.profile_image')
    call_number = serializers.CharField(
        source='bussiness.user.call_phone_number')
    whatsapp_number = serializers.CharField(
        source='bussiness.user.whatsapp_phone_number')

    class Meta:
        model = BussinessPost
        fields = ['id', 'bussiness', 'account_profile', 'user_name', 'account_name', 'call_number',
                  'whatsapp_number', 'business_location', 'caption', 'post_photos']


class UpdatePostSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(
        style={'base_template': 'textarea.html'}, required=False)
    active = serializers.BooleanField(required=False)

    class Meta:
        model = BussinessPost
        fields = ['id', 'caption', 'active']
