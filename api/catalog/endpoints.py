from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()

router.register('products',api.ProductModelViewSet,basename="honeys")
router.register('my-items/product-photos',api.ProductPhotosModelViewSet,basename="honey-photos")
router.register('product-compositions',api.CompositionsModelViewSet,basename="compositions")
router.register('my-items/product-set-photos',api.SetPhotoViewSet ,basename="set-photos")
router.register('my-items/products',api.MyProductsModelViewSet,basename="my-products")
router.register('create-favorites',api.CreateFavoriteView,basename="favorites")
router.register('product-favorites',api.ProductFavoritesModelViewSet,basename="favorites")

urlpatterns = [
    path('', include(router.urls)),
]