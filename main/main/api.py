from django_filters import rest_framework as filters

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .filters import GoodFilter
from .models import Good
from .permissions import IsGoodEditor, IsGoodAdder
from .serializers import GoodSerializer


class GoodViewSet(viewsets.ModelViewSet):
    """
    Class for providing API for Goods
    """
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    filterset_class = GoodFilter
    filter_backends = (filters.backends.DjangoFilterBackend, OrderingFilter)


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsGoodAdder]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsGoodEditor]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

