from rest_framework import viewsets

from .models import Good
from .serializers import GoodSerializer


class GoodViewSet(viewsets.ModelViewSet):
    """
    Class for providing API for Goods
    """
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
