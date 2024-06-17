from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register('equipment',api.EquipmentModelViewSet,basename="Equipment")
router.register('my-items/equipment-photos',api.EquipmentPhotosModelViewSet,basename="Equipment-photos")
router.register('equipment-categories',api.CategoryModelViewSet,basename="Equipment-categories")
router.register('my-items/equipments',api.MyEqipmentsModelViewSet,basename="My-equipment")
router.register('equipment-favorites',api.EquipmentFavoritesModelViewSet,basename="equipment")

urlpatterns = [
    path('', include(router.urls)),
]