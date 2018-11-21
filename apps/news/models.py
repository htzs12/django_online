from django.db import models


class NewsCategorty(models.Model):
    name = models.CharField(max_length=100,verbose_name='新闻分类')
