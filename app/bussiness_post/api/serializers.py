from rest_framework import serializers
from app.bussiness_post.models import BussinessPost, PostImage


class CreatePostSerializer(serializers.ModelSerializer):
    filename = serializers.ListField(child=serializers.ImageField(allow_empty_file=False))
    
    class Meta:
        model = BussinessPost
        fields = ['bussiness', 'caption', 'filename']

    def create(self, validated_data):
        bussiness = self.validated_data['bussiness']
        caption = self.validated_data['caption']
        filename=validated_data.pop('filename')
        
        # save post
        windowshoppi_post = BussinessPost.objects.create(
            bussiness = bussiness,
            caption = caption,
        )

        # save post images
        image_list = []
        for image in filename:
            image_list.append(PostImage(post=windowshoppi_post, filename=image))
        PostImage.objects.bulk_create(image_list)

        return windowshoppi_post


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['post','filename']


class BussinessPostSerializer(serializers.ModelSerializer):
    post_photos = PostImageSerializer(many=True)

    class Meta:
        model = BussinessPost
        fields = ['id', 'caption', 'date_posted', 'date_modified', 'post_photos']