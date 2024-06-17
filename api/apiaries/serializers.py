from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from phonenumber_field import serializerfields

from rest_registration.api.serializers import DefaultUserProfileSerializer

from apps.product.apiaries.models import Apiaries,ApiariesPhotos,BookedDays,ApiariesFavorites



class BookedDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedDays
        fields = ('id','start_day','end_day')



class ApiariesPhotosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiariesPhotos
        fields = ('id','photo')



class ApiariesPhotosCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiariesPhotos
        fields = ('id','photo','item')




class ApiariesSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='_type',read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    booked_days = BookedDaysSerializer(
        many=True,
        required=False
        )
    photos = ApiariesPhotosListSerializer(
        many=True,
        read_only=True
        )
    owner_user = DefaultUserProfileSerializer(read_only=True,source="owner")
    
    class Meta:
        model = Apiaries
        fields = '__all__'

        read_only_fields = ('raiting','is_popular','is_new','discount_price')

    def create(self, validated_data):
        booked_days = validated_data.pop('booked_days',[])
        apiaries = Apiaries.objects.create(**validated_data)
        for day in booked_days:
            BookedDays.objects.create(apiaries=apiaries,**day)

        return apiaries    

    def is_favorite(self, obj):
        user = self.context['request'].user
        
        if user.is_authenticated:
            favorite_items = [item.apiaries for item in user.apiaries_favorites.all()] 
        
            if obj in favorite_items:
                return True
        
            else:
                return False
        
        return None
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_favorite'] = self.is_favorite(instance)
        return representation

class SetPhotoSerializer(serializers.Serializer):
    set_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000,allow_empty_file=False,use_url=True),
        write_only=True,
        )
    apiaries = serializers.PrimaryKeyRelatedField(
        queryset = Apiaries.objects.all(),
    )

    def create(self, validated_data):
        apiaries = validated_data.pop('apiaries')
        for image in validated_data.get('set_images',[]):
            ApiariesPhotos.objects.create(item=apiaries,photo=image)

        return apiaries


class ApiariesFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    apiaries = ApiariesSerializer(read_only=True)
    class Meta:
        model = ApiariesFavorites
        fields = '__all__'

