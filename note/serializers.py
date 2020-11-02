from rest_framework import serializers
from .models import *

class MyNoteSer(serializers.Serializer):
    text = serializers.CharField()

class NoteSer(serializers.Serializer):
    id = serializers.IntegerField()