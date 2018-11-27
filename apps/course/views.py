from django.shortcuts import render
from .models import Course


def course_index(request):
    courses = Course.objects.select_related('teacher','category').all()
    return render(request,'course/course_index.html',locals())


def course_detail(request,course_id):
    course = Course.objects.select_related('teacher','category').get(id=course_id)
    return render(request,'course/course_detail.html',locals())
