from django.shortcuts import render,reverse,redirect
from apps.xfzauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group
from apps.xfzauth.decorators import xfz_superuser_required
from django.utils.decorators import method_decorator
from django.contrib import messages


def staffs_views(request):
    staffs = User.objects.filter(is_staff=True)
    return render(request,'cms/staffs.html',locals())


@method_decorator(xfz_superuser_required,name='dispatch') # 装饰到dispatch
class AddStaffView(View):
    def get(self,request):
        groups = Group.objects.all()
        return render(request,'cms/add_staff.html',locals())

    def post(self,request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            group_ids = request.POST.getlist('groups')  # 获取所有选中值
            groups = Group.objects.filter(pk__in=group_ids)
            user.groups.set(groups)
            user.save()
            return redirect(reverse('cms:staffs'))
        else:
            messages.info(request,'手机号码不存在！')
            return redirect(reverse('cms:add_staffs'))