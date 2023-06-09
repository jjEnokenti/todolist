import django.core.exceptions as django_exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import (
    exceptions,
    serializers,
)

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """User create serializer.

    override create method for passport validation.
    """
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat',
            'role'
        )
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
            raise serializers.ValidationError(
                detail=error_dict
            )

        validated_data['password'] = make_password(password)

        if validated_data.get('role') and validated_data.get('role') == 'admin':
            validated_data['is_staff'] = True

        return super().create(validated_data=validated_data)


class UserListSerializer(serializers.ModelSerializer):
    """User list serializer."""
    class Meta:
        model = User
        exclude = ('password',)


class UserLoginSerializer(serializers.ModelSerializer):
    """User login serializer."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data) -> User | exceptions.AuthenticationFailed:
        """User login logic."""

        username = validated_data.get('username')
        password = validated_data.get('password')

        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            return user

        raise exceptions.AuthenticationFailed('Incorrect password or username.')


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }


class UserChangePasswordSerializer(serializers.Serializer):
    """User change password serializer."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def save(self, **kwargs) -> User:
        """Override save method for validation old and new passwords."""
        user = self.context['request'].user

        old_password = self.validated_data.get('old_password')
        new_password = self.validated_data.get('new_password')

        if not user.check_password(old_password):
            error_dict = {'current password': 'incorrect current password.'}
            error = serializers.ValidationError
            error.default_detail = error_dict
            raise error

        try:
            validate_password(password=new_password)
        except django_exceptions.ValidationError as error:
            error_dict = {'password': error.messages}
            raise serializers.ValidationError(detail=error_dict)

        user.set_password(new_password)

        user.save()

        return user
