from django.urls import reverse
import pytest
from main.models import Category, Good, Seller, Manufacturer
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission


@pytest.mark.parametrize('param', [
    ('index'),
    ('goods')
])
@pytest.mark.django_db
def test_pages(client, param):
    url = reverse(param)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_good_detail(client):
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
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_good_edit(client):
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    change_permission = Permission.objects.get(
        codename='change_good')
    view_permission = Permission.objects.get(
        codename='view_good')
    user.user_permissions.add(change_permission, view_permission)
    user.save()
    client.login(username='testuser', password='12345')
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
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile(client):
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()
    client.login(username='testuser', password='12345')
    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_good_create(client):
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    add_permission = Permission.objects.get(
        codename='add_good')
    view_permission = Permission.objects.get(
        codename='view_good')
    user.user_permissions.add(add_permission, view_permission)
    user.save()
    client.login(username='testuser', password='12345')
    url = reverse('good-add')
    response = client.get(url)
    assert response.status_code == 200