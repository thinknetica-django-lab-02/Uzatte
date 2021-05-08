from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Category, Good, Manufacturer, Seller


class GoodSerializer(ModelSerializer):
    """
    Serializer for Goods
    """
    category = SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    manufacturer = SlugRelatedField(queryset=Manufacturer.objects.all(), slug_field='name')
    seller = SlugRelatedField(queryset=Seller.objects.all(), slug_field='name')

    class Meta:
        model = Good
        fields = ('name', 'price', 'category', 'manufacturer', 'seller', 'tags', 'description')
        depth = 1
