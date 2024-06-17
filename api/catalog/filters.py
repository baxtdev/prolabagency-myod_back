from django_filters import filters,FilterSet

from apps.product.catalog.models import  Product,Compositions

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name':['icontains'],
            'description':['icontains'],
            'price':['lte','gte'],
            'owner':['exact'],
            'is_popular':['exact'],
            'is_new':['exact'],
            'raiting':['lte','gte'],
            'composition':['exact'],

        }


class CompositionsFilter(FilterSet):
    class Meta:
        model = Compositions
        fields = {
            'name':['icontains'],
            'description':['icontains'],
            }
        

