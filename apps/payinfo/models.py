from django.db import models
from shortuuidfield import ShortUUIDField


class PayInfo(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    profile = models.CharField(max_length=200,verbose_name='简介')
    price = models.FloatField(verbose_name='价格')
    path = models.FilePathField(path='images/',verbose_name='路径')


class PayInfoOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    payinfo = models.ForeignKey("PayInfo", on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey("xfzauth.User", on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1：代表的是支付宝支付。2：代表的是微信支付
    istype = models.SmallIntegerField(default=0)
    # 1：代表的是未支付。2：代表的是支付成功
    status = models.SmallIntegerField(default=1)