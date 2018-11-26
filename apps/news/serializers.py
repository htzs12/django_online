from rest_framework import serializers
from apps.news.models import News,NewsCategorty,Comment,Banner
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


class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializers()

    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id','image_url','priority','link_to')