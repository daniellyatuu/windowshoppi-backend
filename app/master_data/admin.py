from django.contrib import admin
from .models import Country, HashTag


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'ios2', 'language',
                    'country_code', 'timezone', 'flag', 'active', 'date_registered']


class HashTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'visited', 'active', 'date_registered']
    search_fields = ['name']


admin.site.register(Country, CountryAdmin)
admin.site.register(HashTag, HashTagAdmin)
