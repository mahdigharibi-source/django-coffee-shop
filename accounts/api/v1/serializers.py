from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import CustomUser


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