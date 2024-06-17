from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from phonenumber_field import serializerfields

from rest_registration.api.serializers import DefaultUserProfileSerializer

from apps.product.equipments.models import Equipment,EquipmentPhotos,Category,EquipmentFavorites


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EquipmentListPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentPhotos
        fields = ('id','photo')


class EquipmentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='_type',read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    photos = EquipmentListPhotosSerializer(
        many=True,
        read_only=True
    )
    owner_user = DefaultUserProfileSerializer(read_only=True,source="owner")
    set_images = serializers.ListField(child=serializers.ImageField(
        max_length=1000000,
        allow_empty_file=False,
        use_url=True),
        write_only=True,)
    
    class Meta:
        model = Equipment
        fields = '__all__'
        read_only_fields = ('raiting','is_new','is_popular','discount_price')


    def create(self, validated_data):
        photos = validated_data.pop('set_images',[])
        
        equipment = Equipment.objects.create(**validated_data)

        for image in photos:
            print(image)
            EquipmentPhotos.objects.create(item=equipment,photo=image)

        return equipment

    def is_favorite(self, obj):
        user = self.context['request'].user
        
        if user.is_authenticated:
            favorite_items = [item.equipment for item in user.equipment_favorites.all()] 
        
            if obj in favorite_items:
                return True
        
            else:
                return False
        
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_favorite'] = self.is_favorite(instance)
        return representation

class EquipmentCreatePhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentPhotos
        fields = '__all__'



class EquipmentFavoritesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    equipment = EquipmentSerializer(read_only=True)

    class Meta:
        model = EquipmentFavorites
        fields = '__all__'