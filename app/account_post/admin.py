from django.contrib import admin
from .models import AccountPost, PostImage


class AccountPostAdmin(admin.ModelAdmin):
    list_display = [
        'account',
        'caption',
        'post_type',
        'recommendation_name',
        'recommendation_type',
        'recommendation_phone_iso_code',
        'recommendation_phone_dial_code',
        'recommendation_phone_number',
        'url',
        'url_action_text',
        'is_url_valid',
        'active',
        'error_happened_on_uploading_image',
        'date_posted',
    ]

    search_fields = [
        'account__name'
    ]


class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        'post',
        'filename',
    ]


admin.site.register(AccountPost, AccountPostAdmin)
admin.site.register(PostImage, PostImageAdmin)
