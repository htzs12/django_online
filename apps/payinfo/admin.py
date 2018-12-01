from django.contrib import admin
from .models import PayInfo


@admin.register(PayInfo)
class PayInfoAdmin(admin.ModelAdmin):
    list_display = ['title','profile','price','path']


