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

 
class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = SocialSerializer
    permission_classes = [permissions.AllowAny]
 
    def post(self, request):
        """Authenticate user through the provider and access_token"""
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
                "uid": authenticated_user.id
            }
            return Response(status=status.HTTP_200_OK, data=response)



class Register(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        s = LoginRegUsers(data=request.data)
        if s.is_valid():
            email = s.validated_data['email']
            pwd = s.validated_data['password']
            if User.objects.filter(email = email).exists():
                return Response({'status': "already to exists"}, status=HTTP_400_BAD_REQUEST)
            else:
                rand = random.randint(1000, 9999)
                u = User.objects.create(email=email, code=f"rand")
                u.set_password(pwd)
                u.save()
                message = "code: " + str(rand)
                send_mail(
                    'Book writer',
                    message,
                    'akinakinov18@gmail.com',
                    [email,],
                    fail_silently=False,
                )
                return Response({'status': "ok", "uid": u.id}, status=HTTP_200_OK)
        else:
            return Response(s.errors, status=HTTP_400_BAD_REQUEST)


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
                return Response({'status': "ok", "key": t.key, "email": u.email, "uid": u.id}, status=HTTP_200_OK)
            else:
                return Response({"status": "wrong code"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(s.errors, status=HTTP_400_BAD_REQUEST)


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
                    return Response({"status": "email or password is wrong"}, status=HTTP_400_BAD_REQUEST)
                # rand = random.randint(1000, 9999)
                t, _ = Token.objects.get_or_create(user=user)
                return Response({'status': "ok", "key": t.key, "uid": user.id, "email": user.email}, status=HTTP_200_OK)
            else:
                return Response({'status': "not find"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(s.errors, status=HTTP_400_BAD_REQUEST)


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
                return Response({'status': "ok", "uid": user.id}, status=HTTP_200_OK)
            else:
                return Response({"status": "not found"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(s.errors, status=HTTP_400_BAD_REQUEST)


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
                return Response({'status': "ok"}, status=HTTP_200_OK)
            else:
                return Response({'status': "incorrect password"}, status=HTTP_200_OK)
        else:
            return Response(s.errors, HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSer
    queryset = User.objects.all()