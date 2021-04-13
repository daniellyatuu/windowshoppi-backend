from .models import Account, Follow
from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'group', 'name', 'account_bio', 'business_bio',
                    'location_name', 'date_registered', 'selected', 'date_modified']

    search_fields = ['user__username', 'group__name', 'name']


class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower', 'following', 'date_followed']

    search_fields = ['follower__name', 'following__name']


admin.site.register(Account, AccountAdmin)
admin.site.register(Follow, FollowAdmin)
