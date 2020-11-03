from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from .serializers import *
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import random
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from utils.compress import compress_image, base64img
from rest_framework import filters
from books.models import Book

class MyNote(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        q = Note.objects.filter(user=request.user)
        s = GetNoteSer(q, many=True,context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = MyNoteSer(data=request.data)
        if s.is_valid():
            book = Book.objects.get(id=s.validated_data['book'])
            Note.objects.create(text=s.validated_data['text'], user=request.user, book=book)
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)

    def delete(self, request):
        s = NoteSer(data=request.data)
        if s.is_valid():
            q = Note.objects.filter(id=s.validated_data['id'])
            if q.exists():
                q[0].delete()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)