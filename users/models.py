from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


def user_photos_dir(instanse, filename):
    usrnme = f'{instanse.id}'
    folder_name = f"{usrnme}/{datetime.today().strftime('%d_%m_%Y')}/{filename}"
    return folder_name


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to = user_photos_dir, blank=True, null=True, default="default/default.png")
    about = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    is_checked = models.BooleanField(default=False)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)

    favorite_books = models.ManyToManyField("books.Book", related_name="fav")
    read_books = models.ManyToManyField("books.Book", related_name="read")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # objects = CustomUserManager()


    def __str__(self):
        return f"{self.email} - {self.id}"