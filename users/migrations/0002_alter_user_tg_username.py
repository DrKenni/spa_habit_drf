# Generated by Django 4.2.6 on 2023-10-12 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tg_username',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Ник в телеграме'),
        ),
    ]
