from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import NewsCategorty
from utils import restful
from .forms import EditNewsCategoryForm
from django.conf import settings
import os


@staff_member_required(login_url='index')
def index(request):
    return render(request,'cms/index.html')


class WriteNewsView(View):
    def get(self,request):
        categories = NewsCategorty.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'cms/write_news.html',context=context)


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

