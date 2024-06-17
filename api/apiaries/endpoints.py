from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()

router.register('apiaries',api.ApiariesModelViewSet,basename="apiaries")
# router.register('apiaries/booked/days',api.BookedDaysModelViewSet,basename="apiaries-booked-days")
router.register('my-items/apiaries-photos',api.ApiariesPhotosModelViewSet,basename="apiaries-photos")
router.register('my-items/apiaries/set/photos',api.SetPhotoViewSet ,basename="set-photos")
router.register('my-items/apiaries',api.MyApiariesModelViewSet,basename="my-apiaries")
router.register('apiaries-favorites',api.ApiariesFavoritesModelViewSet,basename="apiaries-favorites")

urlpatterns = [
    path('', include(router.urls)),
]