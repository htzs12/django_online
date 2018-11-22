from django.shortcuts import render
from .models import News,NewsCategorty
from django.conf import settings
from utils import restful
from .serializers import NewsSerializers


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.order_by('-pub_time')[0:count]
    categories = NewsCategorty.objects.all()
    return render(request,'news/index.html',locals())


def news_list(request):
    #  通过p参数来指定要获取第几页的数据
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))

    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    # 实现首页点击标签切换
    if category_id == 0:
        newses = News.objects.all()[start:end]
    else:
        newses = News.objects.filter(category_id=category_id)[start:end]
    serializers = NewsSerializers(newses,many=True)
    data = serializers.data
    return restful.result(data=data)


def news_detail(request,news_id):
    return render(request,'news/news_detail.html')


def search(request):
    return render(request,'search/search.html')