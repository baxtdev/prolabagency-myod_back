from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from phonenumber_field import serializerfields

from rest_registration.api.serializers import DefaultUserProfileSerializer

from apps.product.catalog.models import Product, ProductPhotos,Compositions,ProductFavorites
from apps.product.equipments.models import Equipment, EquipmentFavorites
from apps.product.apiaries.models import Apiaries, ApiariesFavorites
from apps.users.models import User



class CompositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compositions
        fields = '__all__'



class ProductPhotosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = ('id','photo')



class ProductPhotosCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = ('id','item','photo')



class ProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='_type',read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    photos = ProductPhotosListSerializer(
        many=True,
        read_only=True
        )
    owner_user = DefaultUserProfileSerializer(read_only=True,source="owner")
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('raiting','is_new','is_popular','discount_price')

    def is_favorite(self, obj):
        user:User = self.context['request'].user
        print(user)
        try :
            favorite_items = [item.product for item in user.product_favorites.all()] 
    
            if obj in favorite_items:
                print("favorite cheking tru")
                return True
        except Exception as e:
            print("favorite cheking false",e)   
        return False
        
       

    def to_representation(self, instance):
        representation = super().to_representation(instance)    
        representation['composition']=CompositionsSerializer(instance.composition,many=True).data
        representation['is_favorite'] = self.is_favorite(instance)
        return representation



class SetPhotoSerializer(serializers.Serializer):
    set_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000,allow_empty_file=False,use_url=True),
        write_only=True,
        )
    product = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
    )
    def create(self, validated_data):
        product = validated_data.pop('product')
        for image in validated_data.get('set_images',[]):
            ProductPhotos.objects.create(item=product,photo=image)

        return product




class ProductFavoritesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductFavorites
        fields = '__all__'



class CreateFavoriteSerializer(serializers.Serializer):
    item = serializers.IntegerField()

    APAI ='apaires'
    PROD ='product'  
    EQUI ='equipments' 

    TYPE_CHOICES = (
        (APAI, 'Apiaries'),
        (PROD, 'Product'),
        (EQUI, 'Equipment'),
    )
    type = serializers.ChoiceField(choices=TYPE_CHOICES)

    def create(self, validated_data):
        item_id = validated_data['item']
        
        user = self.context.get('request').user
        
        favorite_type = validated_data.get('type')
        
        
        if favorite_type == self.PROD:
            return ProductFavorites.objects.get_or_create(
                product=Product.objects.get(id=item_id),
                user=user
            )[0]
        elif favorite_type == self.EQUI:
            return EquipmentFavorites.objects.get_or_create(
                equipment=Equipment.objects.get(id=item_id),
                user=user
            )[0]
        elif favorite_type == self.APAI:
            return ApiariesFavorites.objects.get_or_create(
                apiaries=Apiaries.objects.get(id=item_id),
                user=user
            )[0]
        else:
            raise serializers.ValidationError({"message":"Invalid favorite type"})

