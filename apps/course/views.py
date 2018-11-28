from django.shortcuts import render
from .models import Course,CourseOrder,CourseCategory,Teacher
import time,hmac,os,hashlib
from utils import restful
from django.conf import settings
from apps.xfzauth.decorators import xfz_login_required
from hashlib import md5
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt


def course_index(request):
    # CourseCategory.objects.create(name='浩哥')
    courses = Course.objects.select_related('teacher','category').all()
    return render(request,'course/course_index.html',locals())


def course_detail(request,course_id):
    course = Course.objects.select_related('teacher','category').get(id=course_id)
    return render(request,'course/course_detail.html',locals())


def course_token(request):
    # video：是视频文件的完整链接
    file = request.GET.get('video')

    course_id = request.GET.get('course_id')
    if not CourseOrder.objects.filter(course_id=course_id,buyer=request.user,status=2).exists():
        return restful.params_error(message='请先购买课程！')

    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})


@xfz_login_required
def course_order(request,course_id):
    course = Course.objects.get(id=course_id)
    order = CourseOrder.objects.create(course=course,buyer=request.user,status=1,amount=course.price)
    notify_url = request.build_absolute_uri(reverse('course:notify_view'))
    return_url = request.build_absolute_uri(reverse('course:course_detail',kwargs={'course_id':course.id}))
    return render(request,'course/course_order.html',locals())


@xfz_login_required
def course_order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = '3754a51b87ae8852a7ea40a80a5f0226'
    uid = '90f81d609e404a8837783926'
    orderuid = str(request.user.pk)

    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    return restful.result(data={"key": key})


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    CourseOrder.objects.filter(uid=orderid).update(status=2)
    return restful.ok()