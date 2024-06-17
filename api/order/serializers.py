from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from phonenumber_field import serializerfields

from rest_registration.api.serializers import DefaultUserProfileSerializer

from apps.order.models import ItemReviews, Order,OrderApiaries,OrderEqipments,OrderProducts

from api.catalog.serializers import ProductSerializer
from api.equipments.serializers import EquipmentSerializer
from api.apiaries.serializers import ApiariesSerializer

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ('id','quantity','item','status','item_total')
        read_only_fields = ('status',)


class OrderEqipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEqipments
        fields = ('id','quantity','item','status','item_total')
        read_only_fields = ('status',)




class OrderApiariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderApiaries
        fields = ('id','quantity','item','status','start_date','end_date','item_total')
        read_only_fields = ('status',)


class OrderListSerializer(serializers.ModelSerializer):
    owner = DefaultUserProfileSerializer()
    class Meta:
        model = Order
        fields = (
            'id',
            'owner',
            'created_at',
            'number',
            'name',
            'email',
            'adress',
            'number',
            'total',
            'code_number',
            'phone'
        )


class MyOrderProductSerializer(serializers.ModelSerializer):
    order = OrderListSerializer(read_only=True)
    item = ProductSerializer(read_only= True)
    class Meta:
        model = OrderProducts
        fields = ('id','quantity','item','order','status','item_total')
        read_only_fields = ('id','quantity','item','order')


class MyOrderEqipmentSerializer(serializers.ModelSerializer):
    order = OrderListSerializer(read_only=True)
    item = EquipmentSerializer(read_only=True)
    class Meta:
        model = OrderEqipments
        fields = ('id','quantity','item','order','status','item_total')
        read_only_fields = ('id','quantity','item','order')




class MyOrderApiariesSerializer(serializers.ModelSerializer):
    order = OrderListSerializer(read_only=True)
    item = ApiariesSerializer(read_only=True)
    class Meta:
        model = OrderApiaries
        fields = ('id','quantity','item','order','status','start_date','end_date','item_total')
        read_only_fields = ('id','quantity','item','order','start_date','end_date')




class OrderSerializer(serializers.ModelSerializer):
    items = OrderProductSerializer(
        many=True,
        required=False
        )
    equipments = OrderEqipmentSerializer(
        many=True,
        required=False
        )
    apiaries = OrderApiariesSerializer(
        many=True,
        required=False
        )
    
    owner = DefaultUserProfileSerializer(read_only=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
            'email',
            'phone',
            'adress',
            'owner',
            'items',
            'equipments',
            'apiaries',
            'total'
        )       


    def create(self, validated_data):
        user = self.context['request'].user
        
        if user.is_authenticated:
            validated_data['owner'] = user


        items = validated_data.pop('items',[])
        equipments = validated_data.pop('equipments',[])
        apiaries = validated_data.pop('apiaries',[])

        print(validated_data)
        order = Order.objects.create(**validated_data)


        if items:
            for item in items:
                OrderProducts.objects.create(order=order, **item)

        if equipments:
            for equipment in equipments:
                OrderEqipments.objects.create(order=order, **equipment)

        if apiaries:
            for apiary in apiaries:
                OrderApiaries.objects.create(order=order, **apiary)

        return order     



class OrderProductListSerializer(serializers.ModelSerializer):
    item = ProductSerializer()
    class Meta:
        model = OrderProducts
        fields = ('id','quantity','item','status','item_total')
        read_only_fields = ('status',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = instance.item._type
        return representation

class OrderEqipmentListSerializer(serializers.ModelSerializer):
    item  = EquipmentSerializer()
    class Meta:
        model = OrderEqipments
        fields = ('id','quantity','item','status','item_total')
        read_only_fields = ('status',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = instance.item._type
        return representation



class OrderApiariesListSerializer(serializers.ModelSerializer):
    item = ApiariesSerializer()
    class Meta:
        model = OrderApiaries
        fields = ('id','quantity','item','status','start_date','end_date','item_total')
        read_only_fields = ('status',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = instance.item._type
        return representation


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderProductListSerializer(
        many=True,
        required=False
        )
    equipments = OrderEqipmentListSerializer(
        many=True,
        required=False
        )
    apiaries = OrderApiariesListSerializer(
        many=True,
        required=False
        )
    
    owner = DefaultUserProfileSerializer(read_only=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
            'email',
            'phone',
            'adress',
            'owner',
            'items',
            'equipments',
            'apiaries',
            'total',
            'number',
            'code_number'
        )       
        ref_name = "ListOrder"

class ItemReviewCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ItemReviews
        fields = '__all__'


class ItemReviewListSerializer(serializers.ModelSerializer):
    owner = DefaultUserProfileSerializer()
    product = ProductSerializer()
    equipments = EquipmentSerializer()
    class Meta:
        model = ItemReviews
        fields = '__all__'
