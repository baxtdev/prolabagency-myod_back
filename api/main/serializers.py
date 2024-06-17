from rest_framework.serializers import ModelSerializer

from apps.main.models import FAQ,Advertisement


class FAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class AdvertisementSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        

