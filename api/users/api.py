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


from api.users.serializers import (
    GoogleAuthSerializer, 
    RegisterUserSerializer,
    ResetPasswordSerializer,ResetPasword, 
    UserProfileSerializer,User,
    )
from apps.utils.utils import send_code


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = UserProfileSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })



class GoogleAuthAPIView(GenericAPIView):
    serializer_class =  GoogleAuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = DefaultUserProfileSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })
    
    
class GetResetPasswordCodeAPI(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'email'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user:
            response = ResetPasword.objects.create(
                user=user,
                is_active=True
            )
            
            data = response.code
            res = send_code(data,user.email)
            if res:
                return get_ok_response(('вам отправлен код'))
            else:
                return Response({"detail": "Failed to send code"}, status=500)
        else:
            return Response({"detail": "User not found"}, status=404)



class ChekingCodeAPI(GenericAPIView):
    queryset = ResetPasword.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'code'

    def post(self, request, *args, **kwargs):
        data=self.get_object()
        if data.is_active:
            return get_ok_response("this code is active")
        else:
            return Response({"detail":"this code is not active"},404)



class ResetPasswordAPIView(GenericAPIView):
    queryset = ResetPasword.objects.filter(is_active=True)
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'code'
    serializer_class = ResetPasswordSerializer   

    def get_object(self):
        queryset = self.get_queryset()
        try:
            user = queryset.get(code=self.kwargs['code'])
            return user
        
        except ResetPasword.DoesNotExist:
            raise NotFound("Код не подерживается")

    def post(self, request, *args, **kwargs):
        data_t=datetime.today()
        reset_object = self.get_object()
        if reset_object:
            if reset_object.data==data_t.date():    
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                password=serializer.validated_data.get('password')
                reset_object.user.set_password(password)
                reset_object.user.save()
                reset_object.is_active=False
                reset_object.save()
                reset_object.delete()
                return get_ok_response(("your password is changed"))  
            else:
                return Response({"detail":"this code is inactive"},404)
        else:
            return Response({"detail":"not defound"},400)    


