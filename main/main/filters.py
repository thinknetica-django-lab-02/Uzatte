from django_filters import rest_framework as filters

from .models import Good


class GoodFilter(filters.FilterSet):
    """
    Filter for Goods
    """
    name = filters.CharFilter(lookup_expr='icontains')
    price = filters.NumberFilter()
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lte')
    description = filters.CharFilter()
    description__icontains = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Good
        fields = ['category', 'name', 'price', 'seller', 'manufacturer', 'description']
