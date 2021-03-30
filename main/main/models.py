from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Class that describes Tags
    """
    name = models.CharField('Имя тэга', max_length=50, unique=True)

    def __str__(self):
        """
        Method that return string name of tag
        :return: str
        """
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Category(models.Model):
    """
    Class that describes Categories of Goods
    """
    name = models.CharField('Название категории', max_length=120, unique=True)
    description = models.TextField('Описание категории товаров')

    def __str__(self):
        """
        Method that return string name of Category
        :return: str
        """
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Seller(models.Model):
    """
    Class that describes Seller
    """
    name = models.CharField('Имя продавца', max_length=120, unique=True)
    description = models.TextField('Описание продавца')
    email = models.EmailField('Электронный адрес продавца')
    address = models.TextField('Адрес продавца')

    def __str__(self):
        """
        Method that return string name of Seller
        :return: str
        """
        return self.name

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Manufacturer(models.Model):
    """
    Class that describes Manufacturer
    """
    name = models.CharField('Название производителя', max_length=120,
                            unique=True)
    description = models.TextField('Описание Производетеля')


class Good(models.Model):
    """
    Class that describes Goods
    """
    name = models.CharField('Наименование товара', max_length=120, unique=True)
    description = models.TextField('Описание товара')
    price = models.DecimalField('Цена товара', decimal_places=2, max_digits=10)
    # Set PROTECT because delete of category
    # should not entail delete of a good.
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # Set to CASCADE because delete of seller should entail
    # delete of all it's goods.
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    # Set to CASCADE because delete of Manufacturer should entail
    # delete of all it's goods.
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        """
        Method that return string name of good
        :return: str
        """
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Profile(models.Model):
    """
    Class that describes user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Method that return first and last name of a user
        :return: str
        """
        return self.user.first_name + " " + self.user.last_name
