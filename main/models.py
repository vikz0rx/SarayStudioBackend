import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(db_index=True, unique=True, verbose_name='Электронная почта')
    is_active = models.BooleanField(default=True, verbose_name='Активный аккаунт')
    is_staff = models.BooleanField(default=False, verbose_name='Административный аккаунт')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

class Profile(TimestampedModel):
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    firstname = models.CharField(max_length=32, blank=True, null=True, verbose_name='Имя')
    lastname = models.CharField(max_length=32, blank=True, null=True, verbose_name='Фамилия')
    middlename = models.CharField(max_length=32, blank=True, null=True, verbose_name='Отчество')
    birthdate = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    p_series = models.CharField(max_length=4, blank=True, null=True, verbose_name='Паспорт / Серия')
    p_number = models.CharField(max_length=6, blank=True, null=True, verbose_name='Паспорт / Номер')
    insurance = models.CharField(max_length=11, blank=True, null=True, verbose_name='СНИЛС')
    sms_notification = models.BooleanField(default=True, verbose_name='Оповещение по SMS')
    email_notification = models.BooleanField(default=False, verbose_name='Оповещение по почте')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class BookingTypes(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    cost = models.PositiveSmallIntegerField(verbose_name='Стоимость')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип бронирования'
        verbose_name_plural = 'Бронирования / Типы бронирования'

class BookingOptions(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    cost = models.PositiveSmallIntegerField(verbose_name='Стоимость')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительная услуга'
        verbose_name_plural = 'Бронирования / Дополнительные услуги'

class StuffKind(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория оборудования'
        verbose_name_plural = 'Категории оборудования'

class Stuff(models.Model):
    kind = models.ForeignKey(StuffKind, on_delete=models.CASCADE, related_name='kind', verbose_name='Категория оборудования')
    name = models.CharField(max_length=64, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    cost = models.PositiveSmallIntegerField(verbose_name='Стоимость')
    rent_cost = models.PositiveSmallIntegerField(verbose_name='Стоимость аренды', default=0)
    number = models.PositiveSmallIntegerField(verbose_name='Количество', default=1)
    image = models.ImageField(upload_to='stuff', verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оборудование и другое'
        verbose_name_plural = 'Оборудование и другое'

class Photographs(models.Model):
    firstname = models.CharField(max_length=32, verbose_name='Имя')
    lastname = models.CharField(max_length=32, verbose_name='Фамилия')
    instagram = models.URLField(verbose_name='Instagram')
    bio = models.TextField(verbose_name='Описание')
    cost = models.PositiveSmallIntegerField(verbose_name='Стоимость услуг')
    is_staff = models.BooleanField(default=False, verbose_name='Штатный фотограф')

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'Фотограф'
        verbose_name_plural = 'Фотографы'

class Makeup(models.Model):
    firstname = models.CharField(max_length=32, verbose_name='Имя')
    lastname = models.CharField(max_length=32, verbose_name='Фамилия')
    instagram = models.URLField(verbose_name='Instagram')
    bio = models.TextField(verbose_name='Описание')
    cost = models.PositiveSmallIntegerField(verbose_name='Стоимость услуг')
    is_staff = models.BooleanField(default=False, verbose_name='Штатный визажист')

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'Визажист'
        verbose_name_plural = 'Визажисты'

class Area(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    rent_cost = models.PositiveSmallIntegerField(verbose_name='Стоимость аренды', default=0)
    tax_weekends = models.PositiveSmallIntegerField(verbose_name='+ Выходные', default=0)
    tax_latetime = models.PositiveSmallIntegerField(verbose_name='+ Позднее время', default=0)
    stuff = models.ManyToManyField(Stuff, blank=True, related_name='stuff', verbose_name='Оборудование')
    image = models.ImageField(upload_to='areas', verbose_name='Главное изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Зал и локация'
        verbose_name_plural = 'Залы и локации'

class MultipleImagePhotographs(models.Model):
    relation = models.ForeignKey(Photographs, on_delete=models.CASCADE, verbose_name='Фотограф', related_name='photos')
    image = models.ImageField(upload_to='photograph', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Примеры работ'

class MultipleImageMakeup(models.Model):
    relation = models.ForeignKey(Makeup, on_delete=models.CASCADE, verbose_name='Визажист', related_name='photos')
    image = models.ImageField(upload_to='photograph', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Примеры работ'

class MultipleImageAreas(models.Model):
    relation = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Локация', related_name='photos')
    image = models.ImageField(upload_to='photograph', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'