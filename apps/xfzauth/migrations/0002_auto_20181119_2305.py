# Generated by Django 2.0.5 on 2018-11-19 15:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xfzauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
    ]
