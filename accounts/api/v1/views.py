from django.urls import reverse
from rest_framework import generics, status, views, mixins
import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import EmailMessage
from accounts.api.v1.serializers import RegistrationSerializer, CustomTokenObtainPairSerializer, \
    ChangePasswordSerializer, ActivationResendSerializer, PasswordResetRequestEmailSerializer, \
    PasswordResetTokenVerificationSerializer, SetNewPasswordSerializer
from core import settings
from .serializers import CustomAuthTokenSerializer
from .utils import EmailThread, Util
from ...models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class ProfileApiView(APIView):
    def get(self, request):
        return Response({
            'email': request.user.email,
            'id': request.user.id,
            'is_authenticated': request.user.is_authenticated,
        })


class RegistrationApiView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.validated_data['email'],
            }
            user_obj = get_object_or_404(CustomUser, email=data['email'])
            token = self.get_tokens_for_user(user_obj)

            email_obj = EmailMessage(
                'email/hello.html',
                {'token': token['access']},
                'admin@admin.com',
                to=['mahdionlineee@gmail.com'],
            )
            EmailThread(email_obj).start()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_tokens_for_user(self, user):
        if not user.is_active:
            raise AuthenticationFailed("User is not active")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'id': user.id,
        })


class ApiLogoutTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({'detail': 'Successfully logged out'}, status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ActivationApiView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            token = jwt.decode(kwargs['token'], settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            return Response({'detail': 'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'detail': 'token is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.get(id=token['user_id'])
        if user.is_verified:
            return Response({'messages': 'your account has already been verified'})
        user.is_verified = True
        user.save()
        return Response({'messages': 'your account have been verified'}, status=status.HTTP_200_OK)

class ActivationResendApiView(APIView):
    serializer_class = ActivationResendSerializer
    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.validated_data['user']
            token = self.get_tokens_for_user(user_obj)

            email_obj = EmailMessage(
                'email/hello.html',
                {'token': token['access']},
                'admin@admin.com',
                to=[user_obj.email],
            )
            EmailThread(email_obj).start()
            return Response({'messages': 'user activation resend successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        if not user.is_active:
            raise AuthenticationFailed("User is not active")

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

class PasswordResetRequestEmailApiView(APIView):
    serializer_class = PasswordResetRequestEmailSerializer
    # permission_classes = [IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     serializer = PasswordResetRequestEmailSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = request.user
    #         user.set_password(serializer.validated_data['password'])
    #         user.save()
    #         data = {
    #             'email': user.email,
    #         }
    #         return Response({'detail': data, 'message': "password reset successfully"}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user).access_token
        # relativeLink = reverse('accounts-api-v1:reset-password-validate')
        # current_site = get_current_site(
        #     request=request).domain
        relativeLink = reverse('accounts-api-v1:reset-password-validate')

        print("RELATIVE LINK:", relativeLink)

        current_site = get_current_site(request=request).domain

        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        print("ABS URL:", absurl)
        # absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        # email_body = 'Hi '+user.email + \
        #         'Use the link below to reset your password \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #             'email_subject': 'Verify your email'}

        # Util.send_email(data)
        data = {'email': user.email, "link": absurl, "site": current_site}
        Util.send_templated_email('emails/reset_password_template.html', data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordResetTokenValidateApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = PasswordResetTokenVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"detail": "Token is valid"}, status=status.HTTP_200_OK)


class PasswordResetSetNewApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)












