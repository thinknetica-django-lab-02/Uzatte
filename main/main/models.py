from django.db import models

"""
This model constructed on assume that we have abstract goods and particular
sellers who can sell these goods to clients
Example:
    We have an abstract good like "iPhone 12 Pro" and a list of sellers 
    who can sell it. 
"""


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


class Good(models.Model):
    """
    Class that describes Goods
    """
    name = models.CharField('Наименование товара', max_length=120, unique=True)
    description = models.TextField('Описание товара')
    price = models.DecimalField('Цена товара', decimal_places=2, max_digits=10)
    manufacturer = models.CharField('Производитель товара', max_length=120)

    # Assume that a good can be in several categories
    categories = models.ManyToManyField(Category)
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


class Seller(models.Model):
    """
    Class that describes Seller
    """
    name = models.CharField('Имя продавца', max_length=120, unique=True)
    description = models.TextField('Описание продавца')
    email = models.EmailField('Электронный адрес продавца')
    address = models.TextField('Адрес продавца')
    goods = models.ManyToManyField(Good)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        """
        Method that return string name of Seller
        :return: str
        """
        return self.name

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
