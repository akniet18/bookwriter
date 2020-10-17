from django.urls import path, include
from .views import *

urlpatterns = [
    path('oauth/login/', SocialLoginView.as_view()),
    path("register/", Register.as_view()),
    path("email/validate/", EmailValidated.as_view()),
    path("login/", Login.as_view()),
    path("detail/<pk>", UserDetail.as_view()),

    path("password/forget/email/", ForgotPwdSendEmail.as_view()),
    path("password/forget/change/", PasswordChange.as_view())
]