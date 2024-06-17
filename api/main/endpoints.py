from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()

router.register('FAQ', api.FAQViewSet)
router.register('advertisements', api.AdvertisementViewSet)

urlpatterns = [
    path('',include(router.urls)),
]