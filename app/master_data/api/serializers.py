from rest_framework import serializers
from app.master_data.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'ios2', 'language', 'country_code', 'timezone']
