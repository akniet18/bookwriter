from rest_framework import serializers
from .models import *
from books.serializers import BookSer


class GetNoteSer(serializers.Serializer):
    book = BookSer()
    id = serializers.IntegerField()
    text = serializers.CharField()

class MyNoteSer(serializers.Serializer):
    text = serializers.CharField()
    book = serializers.IntegerField()

class NoteSer(serializers.Serializer):
    id = serializers.IntegerField()