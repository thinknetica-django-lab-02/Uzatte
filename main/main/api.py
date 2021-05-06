from django_filters import rest_framework as filters

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .filters import GoodFilter
from .models import Good
from .serializers import GoodSerializer


class GoodViewSet(viewsets.ModelViewSet):
    """
    Class for providing API for Goods
    """
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    filterset_class = GoodFilter
    filter_backends = (filters.backends.DjangoFilterBackend, OrderingFilter)
