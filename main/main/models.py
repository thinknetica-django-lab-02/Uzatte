import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import Group, User
from django.core import mail
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from phone_field import PhoneField

from .tasks import send_mail_notification

from asgiref.sync import sync_to_async

def birth_date(value: datetime.date) -> None:
    """
    Functions that validate birth_date of User
    """
    now_date = datetime.datetime.now().date()
    difference_in_years = relativedelta(now_date, value).years
    if difference_in_years < 18:
        raise ValidationError('Возраст должен быть больше 18 лет')


class Tag(models.Model):
    """
    Class that describes Tags. Tag is an identifier for categorizing,
    describing, searching for data,
    and setting the internal structure
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
    Class that describes Categories of Goods.
    Categories are logical containers that store
    goods with similar properties
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
    Class that describes Seller. Seller is
    an entity that can be distributor of a good
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
    Class that describes Manufacturer.
    Manufacturer is a entity that manufactured a
    particular good
    """
    name = models.CharField('Название производителя', max_length=120,
                            unique=True)
    description = models.TextField('Описание Производетеля')


class Subscriber(models.Model):
    """
    Class that describes Subscriber.
    Subscriber is a person who want to
    receive mails from Store
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Good(models.Model):
    """
    Class that describes Goods.
    Good is a main entity. Goods are sellable items.
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
    in_stock = models.PositiveIntegerField('В наличии', default=1)
    is_archive = models.BooleanField('В архиве', default=False)
    is_publish = models.BooleanField('Статус публикации', default=False)

    def __str__(self):
        """
        Method that return string name of good
        :return: str
        """
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class GoodProxy(Good):
    class Meta:
        proxy = True
        verbose_name = 'Товар'
        verbose_name_plural = 'Архив товаров'


@receiver(post_save, sender=Good)
def notify_on_good_create(sender: Model, instance,
                          created: bool, **kwargs) -> None:
    """
    Function that send a new mail to Subscriber list
    when a new good created in the store.
    """
    if created:
        email_set = [subscriber.user.email for subscriber
                     in Subscriber.objects.all()]
        subject = 'Новый товар!'
        context = {
            "good_name": instance.name,
        }
        html_message = render_to_string('account/new_good.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'From <one@ecommerce.com>'
        send_mail_notification.delay(subject, plain_message, from_email,
                                     email_set, html_message=html_message)


class Profile(models.Model):
    """
    Class that describes user profile. Extends
    standard user profile with additional fields
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField('Дата рождения пользователя',
                                  validators=[birth_date],
                                  blank=True, null=True)
    image = models.ImageField(upload_to='img', default='default.png',
                              null=True)
    phone_number = PhoneField('Номер телефона пользователя',
                              blank=True)
    phone_confirmed = models.PositiveIntegerField(
        'Флаг подтверждения телефона', default=0)

    def __str__(self):
        """
        Method that return username
        :return: str
        """
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender: Model, instance,
                            created: bool, **kwargs) -> None:
        """
        Function that create user extended user profile and connect it to
        every new user.
        """
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


class SMSlog(models.Model):
    """
    Class that describer sms codes and their status
    We can have many codes on one user if he didn't response
    on first one and request another.
    """
    code = models.PositiveIntegerField('Код подтверждения')
    status = models.CharField('Статус ответа сервера', max_length=14)
    user = models.ManyToManyField(User)


@sync_to_async
def get_good_amount(name):
    try:
        in_stock = Good.objects.get(name=name).in_stock
        if in_stock > 0:
            message = f"This are {in_stock} units of {name} left in stock"
        if in_stock == 0:
            message = f"The good {name } is out of stock"
    except ObjectDoesNotExist:
        message = f"This is no such good as {name}"
    return message
