from django.db import models

from users.models import NULLABLE, User


class Habit(models.Model):
    place = models.CharField(max_length=150, verbose_name='место проведения')
    time = models.TimeField(verbose_name='время проведения')
    action = models.CharField(max_length=200, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак')
    linked = models.ForeignKey('self', verbose_name='связь с привычкой', on_delete=models.SET_NULL, **NULLABLE)
    reward = models.CharField(max_length=200, verbose_name='вознаграждение', **NULLABLE)
    length = models.PositiveSmallIntegerField(verbose_name='продолжительность в сукундах')
    period = models.PositiveSmallIntegerField(verbose_name='переодичность')
    is_public = models.BooleanField(default=False, verbose_name='публичность')
    owner = models.ForeignKey(User, verbose_name='владелец', on_delete=models.CASCADE)

    def __str__(self):
        return f'Мне нужно {self.action} за {self.length} секунд, место: {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
