from django.contrib import admin
from .models import Bussiness


class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        # 'country',
        'bio',
        'location_name',
        'active',
        'date_registered',
    ]

    search_fields = [
        'name',
    ]


admin.site.register(Bussiness, BusinessAdmin)
