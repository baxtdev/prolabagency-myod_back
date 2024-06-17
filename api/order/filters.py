from django_filters import FilterSet

from apps.order.models import ItemReviews


class ItemFilterSet(FilterSet):
    class Meta:
        model = ItemReviews
        fields = {
            'mark':['lte','gte'],
            'comment':['icontains'],
            'product':['exact'],
            'equipments':['exact'],
            'apiaries':['exact'],
            }


