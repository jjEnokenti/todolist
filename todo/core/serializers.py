import django.core.exceptions as django_exceptions
import rest_framework.validators
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import (
    exceptions,
    serializers
)

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'password_repeat',
                  'role']
        extra_kwargs = {
            'id': {'required': False},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password_repeat')

        try:
            validate_password(password=password)
        except django_exceptions.ValidationError as error:
            error_dict = {'password': error.messages}
            raise serializers.ValidationError(detail=error_dict)

        if password_repeat != password:
            error_dict = {
                'password': ['the password and the repeat password must match.']
            }
            raise rest_framework.serializers.ValidationError(
                detail=error_dict
            )

        validated_data['password'] = make_password(password)

        if validated_data.get('role') and validated_data.get('role') == 'admin':
            validated_data['is_staff'] = True

        return super().create(validated_data=validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            return user

        raise exceptions.AuthenticationFailed('Incorrect password or username')


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )
