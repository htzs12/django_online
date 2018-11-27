import os
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import NewsCategorty,News,Banner
from apps.course.models import Course,Teacher,CourseCategory
from apps.news.serializers import BannerSerializer
from utils import restful
from .forms import EditNewsCategoryForm,WriteNewForm,AddBannerForm,EditBannerForm,EditNewsForm,PubCourseForm
from django.conf import settings
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse


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


class NewsListView(View):
    def get(self,request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category') or 0)

        newses = News.objects.select_related('category', 'author').all()
        categories = NewsCategorty.objects.all()

        if start or end:
            if start:
                start_date = datetime.strptime(start,'%Y/%m/%d')
            else:
                start_date = datetime(year=2018,month=11,day=11)

            if end:
                end_date = datetime.strptime(end,'%Y/%m/%d')
            else:
                end_date = datetime.today()

            newses = newses.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))

        if title:
            newses = newses.filter(title__contains=title)

        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses,1)
        page_obj = paginator.get_page(page)

        context_data = self.get_pagination_data(paginator,page_obj)

        context = {
            'categories':categories,
            'newses':newses,
            'page_obj':page_obj,
            'start':start,
            'end':end,
            'title':title,
            'category_id':category_id,
            'url_query':'&'+parse.urlencode({
                'start':start or '',
                'end':end or '',
                'title':title or '',
                'category':category_id or '',
            })
        }

        context.update(context_data)

        return render(request, 'cms/news_list.html', context=context)

    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number  # 当前页码
        num_pages = paginator.num_pages # 总页数

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            'left_pages':left_pages,
            'right_pages':right_pages,
            'current_page':current_page,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'num_pages':num_pages
        }


class EditNewsView(View):
    def get(self,request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(id=news_id)
        categories = NewsCategorty.objects.all()
        return render(request,'cms/write_news.html',locals())

    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            news_id = form.cleaned_data.get('news_id')
            category = NewsCategorty.objects.get(pk=category_id)
            News.objects.filter(id=news_id).update(title=title, desc=desc, thumbnail=thumbnail, content=content,
                                category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
def delete_news(request):
    news_id = request.POST.get('news_id')
    News.objects.filter(id=news_id).delete()
    return restful.ok()


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


class PubCourseView(View):
    def get(self,request):
        context = {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }

        # CourseCategory.objects.create(name='浩哥哥')
        Teacher.objects.create(username='哈哈',avatar='http://www.baidu.com/',jobtitle='ha',profile='hao')

        return render(request,'cms/pub_course.html',context=context)

    def post(self,request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get("cover_url")
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')

            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)

            Course.objects.create(title=title, video_url=video_url, cover_url=cover_url, price=price, duration=duration,
                                  profile=profile, category=category, teacher=teacher)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())