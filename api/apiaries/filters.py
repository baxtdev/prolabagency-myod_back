from django_filters import FilterSet,filters

from apps.product.apiaries.models import Apiaries

class ApiariesFilter(FilterSet):
    class Meta:
        model = Apiaries
        fields = {
            'name':['icontains'],
            'description':['icontains'],
            'price':['lte','gte'],
            'owner':['exact'],
            'is_popular':['exact'],
            'is_new':['exact'],
            'raiting':['lte','gte'],
            'price_for':['exact'],
            'price':['lte','gte'],
            }