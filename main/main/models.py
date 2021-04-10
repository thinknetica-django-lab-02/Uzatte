import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import Group, User
from django.core import mail
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags


def birth_date(value):
    now_date = datetime.datetime.now().date()
    difference_in_years = relativedelta(now_date, value).years
    if difference_in_years < 18:
        raise ValidationError('Возраст должен быть больше 18 лет')


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


class Subscriber(models.Model):
    """
    Class that describes Subscriber
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)


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
    image = models.ImageField(upload_to='img', default='default.png')
    publish_date = models.DateField('Дата добавление товара в магазин',
                                    default=timezone.now)

    def __str__(self):
        """
        Method that return string name of good
        :return: str
        """
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


def notify_on_good_create(sender, instance, created, **kwargs):
    if created:
        email_set = {subscriber.user.email for subscriber in Subscriber.objects.all()}
        subject = 'Новый товар!'
        context = {
            "good_name": instance.name,
        }
        html_message = render_to_string('account/new_good.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'From <one@ecommerce.com>'
        mail.send_mail(subject, plain_message, from_email, email_set,
                       html_message=html_message)


post_save.connect(notify_on_good_create, sender=Good)


class Profile(models.Model):
    """
    Class that describes user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField('Дата рождения пользователя',
                                  validators=[birth_date])
    image = models.ImageField(upload_to='img', default='default.png')

    def __str__(self):
        """
        Method that return username
        :return: str
        """
        return self.user.username

    # Set default group to every new user
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            group, _ = Group.objects.get_or_create(name='common users')
            instance.groups.add(group)
            Profile.objects.create(user_id=instance.id)
            subject = 'Welcome to E-Commerce #1'
            context = {
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "email": instance.email,
            }
            html_message = render_to_string('account/hello_mail.html', context)
            plain_message = strip_tags(html_message)
            from_email = 'From <one@ecommerce.com>'
            to = instance.email

            mail.send_mail(subject, plain_message, from_email, [to],
                           html_message=html_message)
