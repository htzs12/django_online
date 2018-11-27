from django.shortcuts import render
from .models import News,NewsCategorty
from django.conf import settings
from utils import restful
from .serializers import NewsSerializers,CommentSerializers
from django.http import Http404
from .forms import PublicCommentForm
from .models import Comment,Banner
from apps.xfzauth.decorators import xfz_login_required


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category','author').all()[0:count]
    categories = NewsCategorty.objects.all()
    banners = Banner.objects.all()
    return render(request,'news/index.html',locals())


def news_list(request):
    #  通过p参数来指定要获取第几页的数据
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))

    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    # 实现首页点击标签切换
    if category_id == 0:
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.select_related('category','author').filter(category_id=category_id)[start:end]
    serializers = NewsSerializers(newses,many=True)
    data = serializers.data
    return restful.result(data=data)


def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category','author').prefetch_related('comment_set__author').get(pk=news_id)
    except News.DoesNotExist:
        raise Http404
    return render(request,'news/news_detail.html',locals())


def search(request):
    return render(request,'search/search.html')


# @xfz_login_required
# def public_comment(request):
#     form = PublicCommentForm(request.POST)
#     if form.is_valid():
#         news_id = form.cleaned_data.get('news_id')
#         content = form.cleaned_data.get('content')
#         news = News.objects.get(id=news_id)
#         comment = Comment.objects.create(content=content,news=news,author=request.user)
#         serializers = CommentSerializers(comment)
#         data = serializers.data
#         return restful.result(data=data)
#     else:
#         return restful.params_error(message=form.get_errors())


@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(id=news_id)
        Comment.objects.create(content=content,news=news,author=request.user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())
