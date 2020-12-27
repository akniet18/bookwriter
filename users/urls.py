from django.urls import path, include
from .views import *

urlpatterns = [
    path('oauth/apple/', AppleAuth.as_view()),
    path('oauth/login/', SocialLoginView.as_view()),
    path("register/", Register.as_view()),
    path("email/validate/", EmailValidated.as_view()),
    path("login/", Login.as_view()),
    path("detail/<pk>", UserDetail.as_view()),
    path("change/avatar/", ChangeAvatar.as_view()),

    path("password/forget/email/", ForgotPwdSendEmail.as_view()),
    path("password/forget/change/", PasswordChange.as_view()),

    path("private/policy", privatepolicy),
    path("terms/of/use", usersA),
    path("delete", delete)
]