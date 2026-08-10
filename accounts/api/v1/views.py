import jwt
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
from accounts.api.v1.serializers import RegistrationSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer
from core import settings
from .serializers import CustomAuthTokenSerializer
from .utils import EmailThread
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
