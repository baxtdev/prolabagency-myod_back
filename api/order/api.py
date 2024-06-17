from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime

from rest_registration.utils.responses import get_ok_response
from rest_registration.api.serializers import DefaultUserProfileSerializer

from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,ViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_registration.api.views.base import BaseAPIView 
from rest_framework.request import Request

from ..permissions import IsOwnerOrReadOnly
from ..mixins import ReadAndUpdateModelMixin,mixins,GenericViewSet

from .serializers import (
    ItemReviewListSerializer, MyOrderApiariesSerializer, 
    ItemReviewCreateSerializer,MyOrderEqipmentSerializer,
    MyOrderProductSerializer, Order, OrderListSerializer,OrderSerializer,
    OrderProducts,OrderProductSerializer,
    OrderApiaries,OrderApiariesSerializer,
    OrderEqipments,OrderEqipmentSerializer,
    ItemReviews
)
from .permissions import OrderItemPermission
from .filters import ItemFilterSet

class OrderModelViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    


class MyOrderProductViewSet(ReadAndUpdateModelMixin):
    queryset = OrderProducts.objects.all().order_by('-id')
    serializer_class = MyOrderProductSerializer
    permission_classes = [permissions.IsAuthenticated,OrderItemPermission]
    
    def get_queryset(self):
        return OrderProducts.objects.filter(item__owner=self.request.user)
    


class MyOrderApiariesViewSet(ReadAndUpdateModelMixin):
    queryset = OrderApiaries.objects.all().order_by('-id')
    serializer_class = MyOrderApiariesSerializer
    permission_classes = [permissions.IsAuthenticated,OrderItemPermission]

    
    def get_queryset(self):
        return OrderApiaries.objects.filter(item__owner=self.request.user)
    


class  MyOrderEqipmentsViewSet(ReadAndUpdateModelMixin):
    queryset = OrderEqipments.objects.all().order_by('-id')
    serializer_class = MyOrderEqipmentSerializer   
    permission_classes = [permissions.IsAuthenticated,OrderItemPermission]


    def get_queryset(self):
        return OrderEqipments.objects.filter(item__owner=self.request.user)
     


class MyPurchasesViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(email=user.email).union(queryset.filter(owner=user))
        return queryset


class ItemReviewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):
    queryset = ItemReviews.objects.all().order_by('-id')
    serializer_class = ItemReviewCreateSerializer
    filterset_class = ItemFilterSet

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemReviewListSerializer
        else :
            return self.serializer_class


class MyReviewsViewSet(ReadOnlyModelViewSet):
    queryset = ItemReviews.objects.all().order_by('-id')
    serializer_class = ItemReviewListSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=user)
        return queryset
    

class MyItemreviewsViewSet(ReadOnlyModelViewSet):
    queryset = ItemReviews.objects.all().order_by('-id')
    serializer_class = ItemReviewListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(product__owner=user).union(queryset.filter(equipments__owner=user)).union(queryset.filter(apiaries__owner=user))
        return queryset


