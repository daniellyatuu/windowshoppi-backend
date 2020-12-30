from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'name', 'account_bio', 'business_bio',
                    'location_name', 'date_registered', 'selected', 'date_modified']

    search_fields = [
        'user__username',
        'group__name',
        'name',
    ]


admin.site.register(Account, AccountAdmin)
