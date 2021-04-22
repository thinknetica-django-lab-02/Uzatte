from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.test import Client, TestCase
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
                                        manufacturer=Manufacturer.objects.create(
                                            name="test",
                                            description="test",
                                        )
                                        )
        url = reverse('good-detail', kwargs={'pk': test_good.id})
        response = c.get(url)
        self.assertEqual(200, response.status_code)


class GoodEditTestCase(TestCase):
    """
    Test case for editing a good
    """
    def test_get_page(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        change_permission = Permission.objects.get(
            codename='change_good')
        view_permission = Permission.objects.get(
            codename='view_good')
        user.user_permissions.add(change_permission, view_permission)
        user.save()
        c.login(username='testuser', password='12345')
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
                                        manufacturer=Manufacturer.objects.create(
                                            name="test",
                                            description="test",
                                        )
                                        )
        url = reverse('good-edit', kwargs={'pk': test_good.id})
        response = c.get(url)
        self.assertEqual(200, response.status_code)


class ProfileTestCase(TestCase):
    """
    Test case for Profile
    """
    def test_get_page(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        c.login(username='testuser', password='12345')
        url = reverse('profile')
        response = c.get(url)
        self.assertEqual(200, response.status_code)


class GoodCreateTestCase(TestCase):
    """
    Test case for creating a good
    """
    def test_get_page(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        add_permission = Permission.objects.get(
            codename='add_good')
        view_permission = Permission.objects.get(
            codename='view_good')
        user.user_permissions.add(add_permission, view_permission)
        user.save()
        c.login(username='testuser', password='12345')
        url = reverse('good-add')
        response = c.get(url)
        self.assertEqual(200, response.status_code)


class IndexTestCase(TestCase):
    """
    Test index page
    """
    def test_get_page(self):
        url = reverse('index')
        response = c.get(url)
        self.assertEqual(200, response.status_code)
