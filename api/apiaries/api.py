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

from .serializers import (
    ApiariesPhotos, ApiariesPhotosCreateSerializer,ApiariesPhotosListSerializer,
    ApiariesSerializer,Apiaries,
    BookedDaysSerializer,BookedDays, SetPhotoSerializer,
    ApiariesFavorites,ApiariesFavoriteSerializer
    )

from .filters import ApiariesFilter
from ..permissions import ItemPhotosPermission,IsOwnerOrReadOnly
from ..mixins import ListAndDeleteModelMixin


class ApiariesModelViewSet(ReadOnlyModelViewSet):
    queryset = Apiaries.objects.all().order_by('-id')
    serializer_class = ApiariesSerializer
    filterset_class = ApiariesFilter

    # permission_classes = [permissions.IsAuthenticated]


class BookedDaysModelViewSet(ModelViewSet):
    queryset = BookedDays.objects.all()
    serializer_class = BookedDaysSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApiariesPhotosModelViewSet(ModelViewSet):
    queryset = ApiariesPhotos.objects.all()
    serializer_class = ApiariesPhotosCreateSerializer
    permission_classes = [permissions.IsAuthenticated,ItemPhotosPermission]



class SetPhotoViewSet(ViewSet):
    serializer_class = SetPhotoSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            apiaries = serializer.validated_data['apiaries']
            set_images = serializer.validated_data.get('set_images', [])
            for image in set_images:
                ApiariesPhotos.objects.create(item=apiaries, photo=image)
            return Response({"message": "Photos added successfully."}, status=201)
        else:
            return Response(serializer.errors, status=400)

    
class MyApiariesModelViewSet(ModelViewSet):
    queryset = Apiaries.objects.all().order_by('-id')
    serializer_class = ApiariesSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]
    filterset_class = ApiariesFilter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class ApiariesFavoritesModelViewSet(ListAndDeleteModelMixin):
    lookup_field = 'apiaries__id'
    queryset = ApiariesFavorites.objects.all()
    serializer_class = ApiariesFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
