from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from django.shortcuts import redirect,reverse
from django.http import HttpResponse
from .forms import LoginForm
from utils import restful
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from utils.aliyunsdk import aliyunsms
from django.core.cache import cache
from .forms import RegisterForm
from django.contrib.auth import get_user_model

User = get_user_model()


@require_POST
def login_view(request):
    # 登录函数
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        telephone = login_form.cleaned_data.get('telephone')
        password = login_form.cleaned_data.get('password')
        remember = login_form.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)  # django默认过期时间为２周
                else:
                    request.session.set_expiry(0)  # 关闭浏览器即过期
                return restful.ok()
            else:
                return restful.un_auth(message='您的账户未激活！')
        else:
            return restful.params_error(message='手机号或者密码错误！')
    else:
        errors = login_form.get_errors()
        return restful.params_error(message=errors)


def logout_view(request):
    # 退出
    logout(request)
    return redirect(reverse('index'))


def img_captcha(request):
    # 图片验证码
    text,image = Captcha.gene_code()
    out = BytesIO()  # BytesIO相当于一个管道，用类似储存图片的流数据
    image.save(out,'png')  # 调用image的save方法，将这个image对象保存到BytesIO中
    out.seek(0)  # 将BytesIO的文件指针一道最开始的位置

    response = HttpResponse(content_type='image/png')
    #  从BytesIO管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()  # 读取图片大小

    cache.set(text.lower(),text.lower(),5*60)

    return response


def sms_captcha(request):
    # 短信验证码
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    cache.set(telephone,code,5*60)
    # result = aliyunsms.send_sms(telephone,code) 测试不开启
    # result = aliyunsms.send_sms('18855224160','1234')
    # print(result)
    print('短信验证码',code)
    return restful.ok()


@require_POST
def register(request):
    #  注册
    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
        telephone = register_form.cleaned_data.get('telephone')
        username = register_form.cleaned_data.get('username')
        password = register_form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        user.save()
        login(request,user)
        return restful.ok()
    else:
        return restful.params_error(message=register_form.get_errors())


# def cache_test(request):
#     cache.set('username','haoge',60)
#     result = cache.get('username')
#     print(result)
#     return HttpResponse('success')
