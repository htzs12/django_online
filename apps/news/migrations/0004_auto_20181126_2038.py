# Generated by Django 2.0.5 on 2018-11-26 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20181125_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=0, verbose_name='排序')),
                ('image_url', models.URLField(verbose_name='图片地址')),
                ('link_to', models.URLField(verbose_name='点击地址')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
        ),
        migrations.AlterField(
            model_name='news',
            name='pub_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
    ]