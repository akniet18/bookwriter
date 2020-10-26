from django.urls import path, include
from .views import *

urlpatterns = [
    path("", BookView.as_view({'get': 'list'})),
    path("my/", MyBookView.as_view()),
    path("most/viewed/", MostViewedBooks.as_view({'get': 'list'})),
    path("chapter/<id>", ChapterView.as_view()),
    path("text/<id>", TextView.as_view()),

    path('favs/', FavsBooks.as_view()),
]