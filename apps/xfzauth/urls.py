from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
    path('login/',views.login_view,name='login')
]
