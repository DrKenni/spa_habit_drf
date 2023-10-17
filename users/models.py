from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    tg_chat_id = models.CharField(max_length=35, verbose_name='чат id', **NULLABLE)
    tg_username = models.CharField(max_length=100, unique=True, verbose_name='Ник в телеграме', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
