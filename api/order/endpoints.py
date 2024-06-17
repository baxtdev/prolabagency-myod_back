from django.urls import path, include
from rest_framework import routers

from . import api

router = routers.DefaultRouter()

router.register('orders',api.OrderModelViewSet)
router.register('my-orders-products',api.MyOrderProductViewSet)
router.register('my-orders-apiaries',api.MyOrderApiariesViewSet)
router.register('my-orders-equipments',api.MyOrderEqipmentsViewSet)
router.register('my-purchases',api.MyPurchasesViewSet,basename="my-purchases")
router.register('items-reviews',api.ItemReviewViewSet)
router.register('my-reviews',api.MyReviewsViewSet)
router.register('my-items/reviews',api.MyItemreviewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]