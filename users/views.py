from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from rest_framework import generics, permissions, status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from requests.exceptions import HTTPError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from .serializers import *
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import random
from django.core.mail import send_mail
from django.conf import settings
from utils.compress import compress_image, base64img
import requests
from datetime import timedelta
from django.utils import timezone
from social_core.utils import handle_http_errors
import jwt


class SocialLoginView(generics.GenericAPIView):
    serializer_class = SocialSerializer
    permission_classes = [permissions.AllowAny]
 
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)
        try:
            backend = load_backend(strategy=strategy, name="facebook",
            redirect_uri=None)
        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            authenticated_user = backend.do_auth(access_token, user=user)
        
        except HTTPError as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except AuthForbidden as error:
            return Response({
                "error":"invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
 
        if authenticated_user and authenticated_user.is_active:
            #generate JWT token
            # login(request, authenticated_user)
            token, _ = Token.objects.get_or_create(user=authenticated_user)
            # data={
            #     "token": jwt_encode_handler(
            #         jwt_payload_handler(user)
            #     )}
            #customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "key": token.key,
                "uid": authenticated_user.id,
                "status": 'ok'
            }
            return Response(status=status.HTTP_200_OK, data=response)




class AppleOAuth2(BaseOAuth2):
    """apple authentication backend"""

    name = 'apple'
    ACCESS_TOKEN_URL = 'https://appleid.apple.com/auth/token'
    SCOPE_SEPARATOR = ','
    ID_KEY = 'uid'

    @handle_http_errors
    def do_auth(self, access_token, *args, **kwargs):
        """
        Finish the auth process once the access_token was retrieved
        Get the email from ID token received from apple
        """
        response_data = {}
        client_id, client_secret = self.get_key_and_secret()

        headers = {'content-type': "application/x-www-form-urlencoded"}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': access_token,
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://example-app.com/redirect'
        }

        res = requests.post(AppleOAuth2.ACCESS_TOKEN_URL, data=data, headers=headers)
        response_dict = res.json()
        id_token = response_dict.get('id_token', None)

        if id_token:
            decoded = jwt.decode(id_token, '', verify=False)
            response_data.update({'email': decoded['email']}) if 'email' in decoded else None
            response_data.update({'uid': decoded['sub']}) if 'sub' in decoded else None

        response = kwargs.get('response') or {}
        response.update(response_data)
        response.update({'access_token': access_token}) if 'access_token' not in response else None

        # kwargs.update({'response': response, 'backend': self})
        return Response(response)

    def get_user_details(self, response):
        email = response.get('email', None)
        # token, _ = Token.objects.get_or_create(user=authenticated_user)
        details = {
            'email': email,
        }
        return details

    def get_key_and_secret(self):
        headers = {
            'kid': settings.SOCIAL_AUTH_APPLE_ID_KEY
        }
        payload = {
            'iss': settings.SOCIAL_AUTH_APPLE_ID_TEAM,
            'iat': timezone.now(),
            'exp': timezone.now() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': settings.SOCIAL_AUTH_APPLE_ID_CLIENT,
        }
        client_secret = jwt.encode(
            payload, 
            settings.SOCIAL_AUTH_APPLE_SECRET, 
            algorithm='ES256', 
            headers=headers
        ).decode("utf-8")
        
        return settings.CLIENT_ID, client_secret


class AppleAuth(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        s = SocialSerializer(data=request.data)
        if s.is_valid():
            access_token = s.validated_data['access_token']
            appleAuth = AppleOAuth2()
            res = appleAuth.do_auth(access_token)
            print(res)
            return Response({"status":"ok"})
        else:
            return Response(s.errors)


class Register(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        s = LoginRegUsers(data=request.data)
        if s.is_valid():
            email = s.validated_data['email']
            pwd = s.validated_data['password']
            if User.objects.filter(email = email).exists():
                return Response({'status': "already to exists"})
            else:
                rand = random.randint(1000, 9999)
                u = User.objects.create(email=email, code=f"{rand}")
                u.set_password(pwd)
                u.save()
                message = "code: " + str(rand)
                send_mail(
                    'Book writer',
                    message,
                    settings.EMAIL_HOST_USER,
                    [email,],
                    fail_silently=False,
                )
                return Response({'status': "ok", "uid": u.id})
        else:
            return Response(s.errors)


class EmailValidated(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, requets):
        s = ValidatedEmailSer(data=requets.data)
        if s.is_valid():
            u = User.objects.get(id=s.validated_data['uid'])
            if u.code == s.validated_data['code']:
                t, _ = Token.objects.get_or_create(user=u)
                u.is_checked = True
                u.save()
                return Response({'status': "ok", "key": t.key, "email": u.email, "uid": u.id})
            else:
                return Response({"status": "wrong code"})
        else:
            return Response(s.errors)


class Login(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        s = LoginRegUsers(data=request.data)
        if s.is_valid():
            email = s.validated_data['email']
            pwd = s.validated_data['password']
            user = User.objects.filter(email = email)
            if user.exists():
                user = user[0]
                valid = user.check_password(pwd)
                if not valid:
                    return Response({"status": "email or password is wrong"})
                # rand = random.randint(1000, 9999)
                t, _ = Token.objects.get_or_create(user=user)
                return Response({'status': "ok", "key": t.key, "uid": user.id, "email": user.email})
            else:
                return Response({'status': "not find"})
        else:
            return Response(s.errors)


class ForgotPwdSendEmail(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        s = EmailSer(data=request.data)
        if s.is_valid():
            user = User.objects.filter(email = s.validated_data['email'])
            if user.exists():
                rand = random.randint(1000, 9999)
                user = user[0]
                user.code = rand
                user.save()
                send_mail(
                    'Book writer',
                    f"code: {rand}",
                    'akinakinov18@gmail.com',
                    [s.validated_data['email'],],
                    fail_silently=False,
                )
                return Response({'status': "ok", "uid": user.id})
            else:
                return Response({"status": "not found"})
        else:
            return Response(s.errors)


class PasswordChange(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = PwdSer(data=request.data)
        if s.is_valid():
            pwd = s.validated_data['password']
            user = request.user
            if len(pwd) > 6:
                user.set_password(pwd)
                user.save()
                return Response({'status': "ok"})
            else:
                return Response({'status': "incorrect password"})
        else:
            return Response(s.errors, HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSer
    queryset = User.objects.all()


class ChangeAvatar(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = ChangeAvaSer(data=request.data)
        if s.is_valid():
            avatar = s.validated_data['avatar']
            avatar = base64img(avatar, "ava")
            avatar = compress_image(avatar, (400,400))
            request.user.avatar = avatar
            request.user.save()
            return Response({'status': "ok"})
        else:
            return Response(s.errors)


def privatepolicy(request):
    context = {'context': ""}
    return render(request, 'index.html', context)


def usersA(request):
    context = {'context': ""}
    return render(request, 'index.html', context)


def delete(request):
    context = {'context': ""}
    return render(request, 'index.html', context)