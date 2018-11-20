from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm
from django.http import JsonResponse


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
                return JsonResponse({'code':200,'message':'','data':{}})
            else:
                return JsonResponse({'code':405,'message':'您的账户未激活！','data':{}})
        else:
            return JsonResponse({'code':400,'message':'手机号或者摩玛错误！','data':{}})
    else:
        errors = login_form.get_errors()
        return JsonResponse({'code':400,'message':'','data':errors})


