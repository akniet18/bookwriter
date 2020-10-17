from rest_framework import serializers
from .models import *

class BookSer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    about = serializers.CharField()
    photo = serializers.CharField()

class ChapterSer(serializers.Serializer):
    title = serializers.CharField()

class TextSer(serializers.Serializer):
    text = serializers.CharField()
    
