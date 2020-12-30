from django.contrib import admin
from .models import AccountPost, PostImage


class AccountPostAdmin(admin.ModelAdmin):
    list_display = [
        'account',
        'caption',
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
