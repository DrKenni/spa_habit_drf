# Generated by Django 4.2.6 on 2023-10-16 18:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0004_alter_habit_last_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='last_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 21, 43, 8, 482419), verbose_name='последняя отправка уведомления'),
        ),
    ]