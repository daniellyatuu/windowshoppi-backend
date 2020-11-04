from django.contrib import admin
from .models import BussinessPost, PostImage

class BusinessPostAdmin(admin.ModelAdmin):
    list_display = [
        'bussiness',
        'caption',
        'active',
        'date_posted'
    ]

    search_fields = [
        'bussiness__name'
    ]

class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        'post',
        'filename',
    ]

admin.site.register(BussinessPost, BusinessPostAdmin)
admin.site.register(PostImage, PostImageAdmin)
