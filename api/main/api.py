from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import FAQ,FAQSerializer,Advertisement,AdvertisementSerializer


class FAQViewSet(ReadOnlyModelViewSet):
    queryset = FAQ.objects.all().order_by('order')
    serializer_class = FAQSerializer


class AdvertisementViewSet(ReadOnlyModelViewSet):
    queryset = Advertisement.objects.all().order_by('-id')
    serializer_class = AdvertisementSerializer

