from factory.django import DjangoModelFactory

from .models import Good, Seller


class GoodFactory(DjangoModelFactory):
    """
    Factory for generating Good instances
    """
    class Meta:
        model = Good

    name = "Sample Good"
    manufacturer_id = 1
    price = 73210
    seller_id = 1
    description = "Sample description"
    category_id = 1


class SellerFactory(DjangoModelFactory):
    """
    Factory for generating Seller instances
    """
    class Meta:
        model = Seller

    name = "Sample Seller"
    description = "Sample description"
    email = "email@sample.com"
    address = "sample address"
