from django.urls import path, include
from .views import *

urlpatterns = [
    path("", BookView.as_view({'get': 'list'})),
    path("my/", MyBookView.as_view()),
    path("chapter/<id>", ChapterView.as_view()),
    path("text/<id>", TextView.as_view())
]