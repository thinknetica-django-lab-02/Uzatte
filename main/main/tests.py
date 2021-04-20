from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import Category, Good, Manufacturer, Seller

c = Client()


class GoodListTestCase(TestCase):
    """
    Test case for goods list
    """
    def test_get_page(self):
        url = reverse('goods')
        response = c.get(url)
        self.assertEqual(200, response.status_code)


class GoodDetailTestCase(TestCase):
    """
    Test Case for good detail
    """
    def test_get_page(self):
        test_good = Good.objects.create(name="Macbook Air 2020",
                                        description="Apple Laptop",
                                        price="120000",
                                        category=Category.objects.create(
                                            name="test",
                                            description="test"
                                        ),
                                        seller=Seller.objects.create(
                                            name="test",
                                            description="test",
                                            email="test@test.com",
                                            address="test"
                                        ),
                                        manufacturer = Manufacturer.objects.create(
                                            name="test",
                                            description="test",
                                        )
                                        )
        url = reverse('good-detail', kwargs={'pk': test_good.id})
        response = c.get(url)
        self.assertEqual(200, response.status_code)
