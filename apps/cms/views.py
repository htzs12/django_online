from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import NewsCategorty,News,Banner
from apps.news.serializers import BannerSerializer
from utils import restful
from .forms import EditNewsCategoryForm,WriteNewForm,AddBannerForm,EditBannerForm
from django.conf import settings
import os


@staff_member_required(login_url='index')
def index(request):
    return render(request,'cms/index.html')


class WriteNewsView(View):
    #  编写新闻
    def get(self,request):
        categories = NewsCategorty.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'cms/write_news.html',context=context)

    def post(self,request):
        form = WriteNewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategorty.objects.get(pk=category_id)
            News.objects.create(title=title,desc=desc,thumbnail=thumbnail,content=content,
                                category=category,author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_GET
def news_category(request):
    categories = NewsCategorty.objects.all()
    context = {
        'categories':categories
    }
    return render(request,'cms/news_category.html',context=context)


@require_POST
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategorty.objects.filter(name=name).exists()
    if not exists:
        NewsCategorty.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在！')


@require_POST
def edit_news_category(request):
    #  新闻分类编辑修改
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategorty.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存在')
    else:
        return restful.params_error(message=form.get_errors())


@require_POST
def delete_news_category(request):
    #  删除新闻分类
    pk = request.POST.get('pk')
    try:
        NewsCategorty.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='该分类不存在')


@require_POST
def upload_file(request):
    #  上传文件
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+name) #  build_absolute_uri方法，提供当前页面地址
    return restful.result(data={'url':url})


def banners(request):
    return render(request,'cms/banners.html')


def banner_list(request):
    banners = Banner.objects.all()
    serialize = BannerSerializer(banners,many=True)
    return restful.result(data=serialize.data)


def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority,image_url=image_url,link_to=link_to)
        return restful.result(data={'banner_id':banner.id})
    else:
        return restful.params_error(message=form.get_errors())


def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(id=banner_id).delete()
    return restful.ok()


def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        id = form.cleaned_data.get('id')
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        Banner.objects.filter(id=id).update(priority=priority,image_url=image_url,link_to=link_to)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())
