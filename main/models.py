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