from rest_framework import serializers
from app.account.models import Account
from rest_framework import status
from app.account_post.models import AccountPost, PostImage


class CreatePostSerializer(serializers.ModelSerializer):
    filename = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False))

    class Meta:
        model = AccountPost
        fields = ['account', 'caption', 'location_name',
                  'latitude', 'longitude', 'filename']

    def create(self, validated_data):
        account = self.validated_data['account']
        caption = self.validated_data['caption']
        location_name = self.validated_data.get('location_name', None)
        latitude = self.validated_data.get('latitude', None)
        longitude = self.validated_data.get('longitude', None)
        filename = validated_data.pop('filename')

        # validate filename
        if len(filename) > 10:
            raise serializers.ValidationError(
                {'filename': ['exceeded the number of upload files']})

        # save post
        windowshoppi_post = AccountPost.objects.create(
            account=account, caption=caption, location_name=location_name, latitude=latitude, longitude=longitude)

        try:
            for image in filename:
                PostImage.objects.create(
                    post=windowshoppi_post, filename=image)

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
    account_name = serializers.CharField(source='account.name')
    group = serializers.CharField(source='account.group')
    account_bio = serializers.CharField(source='account.account_bio')
    business_bio = serializers.CharField(source='account.business_bio')
    # business_location = serializers.CharField(source='bussiness.location_name')
    account_profile = serializers.CharField(source='account.profile_image')
    call_number = serializers.CharField(
        source='account.user.call_phone_number')
    whatsapp_number = serializers.CharField(
        source='account.user.whatsapp_phone_number')

    class Meta:
        model = AccountPost
        fields = ['id', 'account_id', 'username', 'account_name', 'group', 'account_bio', 'business_bio', 'account_profile',
                  'categories', 'call_number', 'whatsapp_number', 'caption', 'location_name', 'date_posted', 'post_photos']


class BussinessPostSerializer(serializers.ModelSerializer):  # will be removed
    post_photos = PostImageSerializer(many=True)
    bussiness = serializers.IntegerField(source='account_id')
    user_name = serializers.CharField(source='account.user')
    account_name = serializers.CharField(source='account.name')
    business_location = serializers.CharField(source='account.location_name')
    account_profile = serializers.CharField(source='account.profile_image')
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
        fields = ['caption', 'active']
