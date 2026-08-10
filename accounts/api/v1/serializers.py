from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import CustomUser, Profile
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password1']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'password': 'passwords dose not match'})

        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1')
        return CustomUser.objects.create_user(**validated_data)



class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is disabled."
            )

        attrs['user'] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.instance

        if attrs.get('new_password1') != attrs.get('new_password2'):
            raise serializers.ValidationError({'detail':'passwords is not match'})

        if not user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError({'old_password':'old password is not match'})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance

class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'email':'email does not exist'})

        if user_obj.is_verified:
            raise serializers.ValidationError({
                'messages': 'user already activated and verified'
            })

        attrs['user'] = user_obj
        return attrs

class PasswordResetRequestEmailSerializer(serializers.Serializer):
    # email = serializers.SerializerMethodField()
    # password = serializers.CharField(required=True)
    # password1 = serializers.CharField(required=True)
    #
    # def get_email(self, obj):
    #     return self.context['request'].user.email
    #
    # def validate(self, attrs):
    #     if attrs.get('password') != attrs.get('password1'):
    #         raise serializers.ValidationError({'password': 'passwords dose not match'})
    #
    #     return super(PasswordResetRequestEmailSerializer, self).validate(attrs)

    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(email=attrs["email"])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "There is no user with provided email"})
        attrs["user"] = user
        return super().validate(attrs)



class PasswordResetTokenVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)

    class Meta:
        model = CustomUser
        fields = ['token']

    def validate(self, attrs):
        token = attrs['token']
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError as identifier:
            return serializers.ValidationError({'detail': 'Token expired'})
        except jwt.exceptions.DecodeError as identifier:
            raise serializers.ValidationError({'detail': 'Token invalid'})

        attrs["user"] = user
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=600)
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    password1 = serializers.CharField(
        min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ['password', 'password1', 'token']

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError(
                {"details": "Passwords does not match"}
            )
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
            user.set_password(password)
            user.save()

            return super().validate(attrs)
        except Exception as e:
            print(type(e))
            print(e)
            raise AuthenticationFailed('The reset link is invalid', 401)