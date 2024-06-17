from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime

from rest_registration.utils.responses import get_ok_response
from rest_registration.api.serializers import DefaultUserProfileSerializer

from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,ViewSet,GenericViewSet
from rest_framework import permissions,mixins
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_registration.api.views.base import BaseAPIView 
from rest_framework.request import Request

from ..permissions import IsOwnerOrReadOnly ,ItemPhotosPermission
from ..mixins import ListAndDeleteModelMixin

from .filters import EqipmentFilter,CategoryFilter
from .serializers import (
    Equipment,EquipmentSerializer,
    EquipmentPhotos,EquipmentCreatePhotosSerializer,
    Category,CategorySerializer,EquipmentFavorites,EquipmentFavoritesSerializer
)

class EquipmentModelViewSet(ReadOnlyModelViewSet):
    queryset = Equipment.objects.all().order_by('-id')
    serializer_class = EquipmentSerializer
    filterset_class = EqipmentFilter



class EquipmentPhotosModelViewSet(ModelViewSet):
    queryset = EquipmentPhotos.objects.all()
    serializer_class = EquipmentCreatePhotosSerializer
    permission_classes = [permissions.IsAuthenticated,ItemPhotosPermission]


class CategoryModelViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter


class MyEqipmentsModelViewSet(ModelViewSet):
    queryset = Equipment.objects.all().order_by('-id')
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly] 
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset



class EquipmentFavoritesModelViewSet(ListAndDeleteModelMixin):
    lookup_field = 'equipment__id'
    queryset = EquipmentFavorites.objects.all()
    serializer_class = EquipmentFavoritesSerializer
    permission_classes = [permissions.IsAuthenticated]
