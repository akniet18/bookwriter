from django.urls import path, include
from .views import *

urlpatterns = [
    path('<lang>', BookView.as_view({'get': 'list'})),
    path('my/', MyBookView.as_view()),
    path('user/<id>', UserBooks.as_view()),
    path('most/viewed/<lang>', MostViewedBooks.as_view({'get': 'list'})),
    path('chapter/<id>', ChapterView.as_view()),
    path('text/<id>', TextView.as_view()),
    path('words/<id>', OptionsApi.as_view()),
    path('track/<id>', TrackApi.as_view()),
    path('add/category/', AddCategory.as_view()),

    path('favs/', FavsBooks.as_view()),
    path('i/read/', IRead.as_view()),
    path('test/', TestApi.as_view())
]