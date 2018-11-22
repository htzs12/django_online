from rest_framework import serializers
from apps.news.models import News,NewsCategorty
from apps.xfzauth.serializers import UserSerializers


class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategorty
        fields = ('id','name')


class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = UserSerializers()

    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','category','author','pub_time')