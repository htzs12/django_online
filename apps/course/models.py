from django.db import models
from shortuuidfield import ShortUUIDField


class CourseCategory(models.Model):
    name = models.CharField(max_length=100,verbose_name='课程分类名')


class Teacher(models.Model):
    username = models.CharField(max_length=100,verbose_name='教师名')
    avatar = models.URLField(verbose_name='主页')
    jobtitle = models.CharField(max_length=100,verbose_name='工作类别')
    profile = models.TextField(verbose_name='简介')


class Course(models.Model):
    title = models.CharField(max_length=200,verbose_name='标题')
    category = models.ForeignKey('CourseCategory',on_delete=models.DO_NOTHING,verbose_name='所属分类')
    teacher = models.ForeignKey("Teacher",on_delete=models.DO_NOTHING,verbose_name='所属老师')
    video_url = models.URLField(verbose_name='视频地址')
    cover_url = models.URLField(verbose_name='封面地址')
    price = models.FloatField(verbose_name='价格')
    duration = models.IntegerField(verbose_name='时长')
    profile = models.TextField(verbose_name='介绍')
    pub_time = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')


class CourseOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    course = models.ForeignKey("Course",on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey("xfzauth.User",on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1：代表的是支付宝支付。2：代表的是微信支付
    istype = models.SmallIntegerField(default=0)
    # 1：代表的是未支付。2：代表的是支付成功
    status = models.SmallIntegerField(default=1)