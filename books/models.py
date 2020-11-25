from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.id} - {self.name}'


def photos_dir(instanse, filename):
    folder_name = f"{instanse.title}/{filename}"
    return folder_name

class Book(models.Model):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="my_book", blank=True, null=True)
    title = models.CharField(max_length=100)
    photo =  models.ImageField(upload_to = photos_dir, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    created_day = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, related_name="books")
    views = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f'{self.id}: {self.title}'

    @property
    def get_photo(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.photo.url)


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapter")
    created_day = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.id}: {self.title} - book_id: {self.book.id}'


class Text(models.Model):
    text = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="content")
    created_day = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'id: {self.id} - book: {self.chapter.book.id} - chapter:{self.chapter.id}'


class Track(models.Model):
    uri = models.CharField(max_length=500, blank=True, null=True)
    audio = models.FileField(upload_to=None, max_length=100, blank=True, null=True)
    track_name = models.CharField(max_length=500, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    ranges = ArrayField(models.FloatField(), blank=True, null=True)
    chapter = models.ForeignKey("books.Chapter", on_delete=models.CASCADE, related_name="tracks")

    def __str__(self):
        return f'{self.chapter.id} - {self.chapter.title}'


class TextOptions(models.Model):
    ranges = ArrayField(models.BigIntegerField())
    color = models.CharField(max_length=50)
    word = models.TextField(blank=True, null=True)
    text = models.ForeignKey("books.Text", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text.id}'