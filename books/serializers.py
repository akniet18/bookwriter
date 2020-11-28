from rest_framework import serializers
from .models import *
from users.serializers import UserDetailSer

class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BookSer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = UserDetailSer(read_only=True)
    title = serializers.CharField()
    about = serializers.CharField()
    photo_url = serializers.SerializerMethodField('get_avatar_url', read_only=True)
    category = CategorySer(read_only=True, many=True)
    # category_id = serializers.IntegerField(write_only=True)
    photo = serializers.CharField(write_only = True)
    views = serializers.IntegerField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)

    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.photo.url)

class ChapterSer(serializers.Serializer):
    title = serializers.CharField()


class TextSer(serializers.Serializer):
    text = serializers.CharField()
    

class BooksId(serializers.Serializer):
    id = serializers.IntegerField()


class AddCategorySer(serializers.Serializer):
    id = serializers.IntegerField()
    categories = serializers.ListField()


class TrackSer(serializers.Serializer):
    audio = serializers.FileField()
    duration = serializers.CharField(required=False)
    ranges = serializers.ListField(required=False)
    track_name = serializers.CharField()


class GettrackSer(serializers.ModelSerializer):
    audio = serializers.SerializerMethodField('get_avatar_url', read_only=True)
    class Meta:
        model = Track
        fields = "__all__"

    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.photo.url)


class OptionsSer(serializers.Serializer):
    ranges = serializers.ListField()
    color = serializers.CharField()
    word = serializers.CharField()
    
