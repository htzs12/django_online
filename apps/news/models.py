from django.db import models



class NewsCategorty(models.Model):
    name = models.CharField(max_length=100,verbose_name='新闻分类')


class News(models.Model):
    title = models.CharField(max_length=200,verbose_name='标题')
    desc = models.CharField(max_length=200,verbose_name='描述信息')
    thumbnail = models.URLField(verbose_name='缩略图')
    content = models.TextField(verbose_name='内容')
    pub_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    category = models.ForeignKey('NewsCategorty',on_delete=models.SET_NULL,null=True,verbose_name='所属分类')
    author = models.ForeignKey('xfzauth.User',on_delete=models.SET_NULL,null=True,verbose_name='所属作者')

    class Meta:
        ordering = ['-pub_time']


class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    pub_time = models.DateTimeField(auto_now_add=True,verbose_name='时间')
    news = models.ForeignKey('News',on_delete=models.CASCADE,verbose_name='所属新闻')
    author = models.ForeignKey('xfzauth.User',on_delete=models.CASCADE,verbose_name='所属用户')

    class Meta:
        ordering = ['-pub_time']


class Banner(models.Model):
    priority = models.IntegerField(default=0,verbose_name='优先级')
    image_url = models.URLField(verbose_name='图片地址')
    link_to = models.URLField(verbose_name='点击地址')
    pub_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    class Meta:
        ordering = ['priority']