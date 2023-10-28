from django.conf import settings
from django.db import models
from datetime import datetime

from users.models import NULLABLE


class Habit(models.Model):
    place = models.CharField(max_length=150, verbose_name='место проведения')
    time = models.TimeField(verbose_name='время проведения')
    action = models.CharField(max_length=200, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак')
    linked = models.ForeignKey('self', verbose_name='связь с привычкой', on_delete=models.SET_NULL, **NULLABLE)
    reward = models.CharField(max_length=200, verbose_name='вознаграждение', **NULLABLE)
    length = models.PositiveSmallIntegerField(verbose_name='продолжительность в сукундах')
    period = models.PositiveSmallIntegerField(verbose_name='переодичность', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='публичность')
    last_time = models.DateTimeField(default=datetime.now(), verbose_name='последняя отправка уведомления')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='владелец', **NULLABLE,)

    def __str__(self):
        return f'Мне нужно {self.action} за {self.length} секунд, место: {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ['id']
