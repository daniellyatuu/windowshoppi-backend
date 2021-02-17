from app.account_post.account_post_background_tasks import verify_url
from app.account_post.models import AccountPost, PostImage
from rest_framework import serializers
from app.account.models import Account
from rest_framework import status
from django.utils import timezone


class CreatePostSerializer(serializers.ModelSerializer):
    filename = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False))

    class Meta:
        model = AccountPost
        fields = ['account', 'caption', 'recommendation_name', 'recommendation_type', 'recommendation_phone_iso_code', 'recommendation_phone_dial_code',
                  'recommendation_phone_number', 'url', 'url_action_text', 'location_name', 'latitude', 'longitude', 'filename', 'post_type']

    def create(self, validated_data):
        account = self.validated_data['account']
        caption = self.validated_data['caption']
        recommendation_name = self.validated_data.get(
            'recommendation_name', None)
        recommendation_type = self.validated_data.get(
            'recommendation_type', None)
        recommendation_phone_iso_code = self.validated_data.get(
            'recommendation_phone_iso_code', None)
        recommendation_phone_dial_code = self.validated_data.get(
            'recommendation_phone_dial_code', None)
        recommendation_phone_number = self.validated_data.get(
            'recommendation_phone_number', None)
        post_type = self.validated_data.get('post_type', None)
        url = self.validated_data.get('url', None)
        url_action_text = self.validated_data.get('url_action_text', None)
        location_name = self.validated_data.get('location_name', None)
        latitude = self.validated_data.get('latitude', None)
        longitude = self.validated_data.get('longitude', None)
        filename = validated_data.pop('filename')

        # validate filename
        if len(filename) > 10:
            raise serializers.ValidationError(
                {'filename': ['exceeded the number of upload files']})

        # save post
        windowshoppi_post = AccountPost.objects.create(account=account, caption=caption, recommendation_name=recommendation_name, recommendation_type=recommendation_type, recommendation_phone_iso_code=recommendation_phone_iso_code,
                                                       recommendation_phone_dial_code=recommendation_phone_dial_code, recommendation_phone_number=recommendation_phone_number, url=url, url_action_text=url_action_text, location_name=location_name, latitude=latitude, longitude=longitude, post_type=post_type)

        try:
            for image in filename:
                PostImage.objects.create(
                    post=windowshoppi_post, filename=image)

            # check if url is saved
            if windowshoppi_post.url:
                # verify url
                verify_url(windowshoppi_post.id)

            return {
                'id': windowshoppi_post.id
            }
        except:
            # make uploaded post inactive if error happen on uploading image(s)
            windowshoppi_post.active = False
            windowshoppi_post.error_happened_on_uploading_image = True
            windowshoppi_post.save()
            return 'error_occurred'


class CreatePostSerializerOld(serializers.ModelSerializer):  # will be removed
    bussiness = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all())
    filename = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False))

    class Meta:
        model = AccountPost
        fields = ['bussiness', 'caption', 'filename']

    def create(self, validated_data):

        account = self.validated_data['bussiness']
        caption = self.validated_data['caption']
        filename = validated_data.pop('filename')

        # validate filename
        if len(filename) > 10:
            raise serializers.ValidationError(
                {'filename': ['exceeded the number of upload files']})

        # save post
        windowshoppi_post = AccountPost.objects.create(
            account=account, caption=caption)

        for image in filename:
            PostImage.objects.create(post=windowshoppi_post, filename=image)

        return True


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['filename']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['filename']


class AccountPostSerializer(serializers.ModelSerializer):
    post_photos = PostImageSerializer(many=True)
    username = serializers.CharField(source='account.user')
    # account_name = serializers.CharField(source='account.name')
    group = serializers.CharField(source='account.group')
    # account_bio = serializers.CharField(source='account.account_bio')
    business_bio = serializers.CharField(source='account.business_bio')
    account_profile = serializers.CharField(source='account.profile_photo')
    recommendation_type = serializers.CharField(
        source='get_recommendation_type_display')
    post_type = serializers.CharField(source='get_post_type_display')
    # call_number = serializers.CharField(
    #     source='account.user.call_phone_number')
    # whatsapp_number = serializers.CharField(
    #     source='account.user.whatsapp_phone_number')

    class Meta:
        model = AccountPost
        # fields = ['id', 'account_id', 'username', 'account_name', 'group', 'account_bio', 'business_bio', 'account_profile',
        #           'categories', 'call_number', 'whatsapp_number', 'caption', 'url', 'url_action_text', 'is_url_valid', 'location_name', 'latitude', 'longitude', 'date_posted', 'post_photos']

        fields = ['id', 'account_id', 'username', 'group', 'business_bio', 'account_profile', 'caption', 'recommendation_name', 'recommendation_type', 'recommendation_phone_iso_code',
                  'recommendation_phone_dial_code', 'recommendation_phone_number', 'url', 'url_action_text', 'is_url_valid', 'location_name', 'latitude', 'longitude', 'date_posted', 'post_photos', 'post_type']


class BussinessPostSerializer(serializers.ModelSerializer):  # will be removed
    post_photos = PostImageSerializer(many=True)
    bussiness = serializers.IntegerField(source='account_id')
    user_name = serializers.CharField(source='account.user')
    account_name = serializers.CharField(source='account.name')
    business_location = serializers.CharField(source='account.location_name')
    account_profile = serializers.CharField(source='account.profile_photo')
    call_number = serializers.CharField(
        source='account.user.call_phone_number')
    whatsapp_number = serializers.CharField(
        source='account.user.whatsapp_phone_number')

    class Meta:
        model = AccountPost
        fields = ['id', 'bussiness', 'account_profile', 'user_name', 'account_name', 'call_number',
                  'whatsapp_number', 'business_location', 'caption', 'post_photos']


class UpdatePostSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(
        style={'base_template': 'textarea.html'}, required=False)
    active = serializers.BooleanField(required=False)

    class Meta:
        model = AccountPost
        fields = ['caption', 'location_name',
                  'latitude', 'longitude', 'active']
