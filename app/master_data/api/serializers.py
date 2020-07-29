from rest_framework import serializers
from app.master_data.models import Country, Category


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'ios2', 'language',
                  'country_code', 'timezone', 'flag']

    def create(self, validated_data):
        name = self.validated_data['name']
        ios2 = self.validated_data['ios2']
        language = self.validated_data['language']
        country_code = self.validated_data['country_code']
        timezone = self.validated_data['timezone']
        flag = validated_data.pop('flag')

        # save post
        country = Country.objects.create(
            name=name,
            ios2=ios2,
            language=language,
            country_code=country_code,
            timezone=timezone,
            flag=flag,
        )

        return country


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
