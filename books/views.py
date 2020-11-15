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


class MyBookView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Book.objects.filter(author=request.user)
        s = BookSer(queryset, many=True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = BookSer(data=request.data)
        if s.is_valid():
            title = s.validated_data['title']
            img = base64img(s.validated_data['photo'], title.replace(" ", ""))
            photo = compress_image(img, (400,400))
            b = Book.objects.create(
                author = request.user,
                title = title,
                about = s.validated_data['about'],
                photo = photo
                # category = Category.objects.get(id=s.validated_data['category_id'])
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class MostViewedBooks(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Book.objects.filter(is_published=True).order_by('-views')
    serializer_class = BookSer


class BookView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Book.objects.filter(is_published=True)
    serializer_class = BookSer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ('title', 'about')
    filter_fields = ('category',)
    

class AddCategory(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = AddCategorySer(data=request.data)
        if s.is_valid():
            book = Book.objects.get(id=s.validated_data['id'])
            c = s.validated_data['categories']
            for i in c:
                cat = Category.objects.get(id=int(i))
                if cat not in book.category.all():
                    book.category.add(cat)
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class UserBooks(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        q = Book.objects.filter(author_id=id, is_published=True)
        s = BookSer(q, many=True, context={'request': request})
        return Response(s.data)

# class Read(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request):



class ChapterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        book = Book.objects.get(id=id)
        book.views += 1
        book.save()
        queryset = book.chapter.values()
        return Response(queryset)

    def post(self, request, id):
        s = ChapterSer(data=request.data)
        if s.is_valid():
            c = Chapter.objects.create(
                title = s.validated_data['title'],
                book_id = id
            )
            Text.objects.create(
                text = " ",
                chapter_id = c.id
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)

    def put(self, request, id):
        s = ChapterSer(data=request.data)
        if s.is_valid():
            c = Chapter.objects.get(id=id)
            c.title = s.validated_data['title']
            c.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class TextView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        # queryset = Chapter.objects.get(id=id).content.values()
        t = Text.objects.get(chapter_id=id)
        op = TextOptions.objects.filter(text=t)
        q = {'text': t.text, "id": t.id}
        words = []
        for i in op:
            words.append({'range': i.ranges, 'color': i.color, 'word': i.word})
        q['words'] = words
        return Response(q)

    def post(self, request, id):
        s = TextSer(data=request.data)
        if s.is_valid():
            t = Text.objects.get(
                chapter_id = id
            )
            t.text = s.validated_data['text']
            t.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)

    def put(self, request, id):
        s = TextSer(data=request.data)
        if s.is_valid():
            t = Text.objects.get(id=id)
            t.text = s.validated_data['text']
            t.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class TrackApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        t = Track.objects.values().filter(chapter_id = id)
        return Response(t)

    def post(self, request, id):
        s = TrackSer(data=request.data)
        if s.is_valid():
            Track.objects.create(uri=s.validated_data['uri'], chapter_id=id, duration=s.validated_data['duration'],
            ranges=s.validated_data.get('ranges', None))
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)

    def delete(self, request, id):
        Track.objects.get(id=id).delete()
        return Response({'status':'ok'})


class OptionsApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, id):
        s = OptionsSer(data=request.data)
        if s.is_valid():
            TextOptions.objects.create(
                ranges = s.validated_data['ranges'],
                color = s.validated_data['color'],
                word = s.validated_data['word'],
                text_id = id
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class FavsBooks(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        books = request.user.favorite_books.all()
        s = BookSer(books, many=True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = BooksId(data=request.data)
        if s.is_valid():
            book = Book.objects.get(id=s.validated_data['id'])
            if book in request.user.favorite_books.all():
                request.user.favorite_books.remove(book)
            else:
                request.user.favorite_books.add(book)
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class IRead(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        books = request.user.read_books.all()
        s = BookSer(books, many=True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = BooksId(data=request.data)
        if s.is_valid():
            book = Book.objects.get(id=s.validated_data['id'])
            if book in request.user.read_books.all():
                request.user.read_books.remove(book)
            else:
                request.user.read_books.add(book)
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)