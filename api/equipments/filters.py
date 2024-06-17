from django_filters import FilterSet,filters

from apps.product.equipments.models import Equipment,Category

class EqipmentFilter(FilterSet):
    class Meta:
        model = Equipment
        fields = {
            'name':['icontains'],
            'description':['icontains'],
            'price':['lte','gte'],
            'owner':['exact'],
            'category':['exact'],
            'raiting':['lte','gte'],
            'is_popular':['exact'],
            'is_new':['exact'],
            }
        

class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'name':['icontains'],
            'description':['icontains'],
            }



