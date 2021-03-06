from rest_framework import serializers
from .models import *


class LoginRegUsers(serializers.Serializer):
	email = serializers.CharField(max_length=50)
	password = serializers.CharField(max_length=20)

class EmailSer(serializers.Serializer):
	email = serializers.CharField(max_length=50)

class PwdSer(serializers.Serializer):
	password = serializers.CharField(max_length=50)

class ValidatedEmailSer(serializers.Serializer):
	uid = serializers.IntegerField()
	code = serializers.CharField(max_length=10)

class SocialSerializer(serializers.Serializer):
    # provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)


class UserDetailSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", 'avatar')
        read_only_fields = ("id", "email", 'avatar')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class ChangeAvaSer(serializers.Serializer):
    avatar = serializers.CharField()