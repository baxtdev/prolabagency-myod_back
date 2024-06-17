from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime

from rest_registration.utils.responses import get_ok_response
from rest_registration.api.serializers import DefaultUserProfileSerializer

from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,ViewSet,GenericViewSet
from rest_framework import permissions,status,mixins
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_registration.api.views.base import BaseAPIView 
from rest_framework.request import Request
from rest_framework.views import APIView


from .filters import ProductFilter, CompositionsFilter
from .serializers import (
    Product, ProductPhotosCreateSerializer,ProductSerializer,
    ProductPhotos,ProductPhotosListSerializer,
    Compositions,CompositionsSerializer, SetPhotoSerializer,
    CreateFavoriteSerializer,ProductFavoritesSerializer,ProductFavorites
)
from ..permissions import ItemPhotosPermission,IsOwnerOrReadOnly
from ..mixins import ListAndDeleteModelMixin


class ProductModelViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter



class ProductPhotosModelViewSet(ModelViewSet):
    queryset = ProductPhotos.objects.all()
    serializer_class = ProductPhotosCreateSerializer
    permission_classes = [permissions.IsAuthenticated,ItemPhotosPermission]



class CompositionsModelViewSet(ReadOnlyModelViewSet):
    queryset = Compositions.objects.all()
    serializer_class = CompositionsSerializer
    filterset_class = CompositionsFilter


class SetPhotoViewSet(ViewSet):
    serializer_class = SetPhotoSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            set_images = serializer.validated_data.get('set_images', [])
            for image in set_images:
                ProductPhotos.objects.create(item=product, photo=image)
            return Response({"message": "Photos added successfully."}, status=201)
        else:
            return Response(serializer.errors, status=400)


class MyProductsModelViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]
    filterset_class = ProductFilter

    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset
    


class CreateFavoriteView(mixins.CreateModelMixin,GenericViewSet):
    serializer_class = CreateFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductFavorites.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            favorite_obj = serializer.create(serializer.validated_data)
            return Response({"success": f"Favorite {favorite_obj} created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


class ProductFavoritesModelViewSet(ListAndDeleteModelMixin):
    lookup_field = 'product__id'
    queryset = ProductFavorites.objects.all()
    serializer_class = ProductFavoritesSerializer
    permission_classes = [permissions.IsAuthenticated]


