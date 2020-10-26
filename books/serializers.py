from rest_framework import serializers
from .models import *

class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BookSer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    about = serializers.CharField()
    photo_url = serializers.SerializerMethodField('get_avatar_url', read_only=True)
    category = CategorySer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    photo = serializers.CharField(write_only = True)
    views = serializers.IntegerField(read_only=True)

    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.photo.url)

class ChapterSer(serializers.Serializer):
    title = serializers.CharField()

class TextSer(serializers.Serializer):
    text = serializers.CharField()
    

class BooksId(serializers.Serializer):
    id = serializers.IntegerField()
