import django.core.exceptions as django_exceptions
import rest_framework.validators
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'role']
        extra_kwargs = {
            'id': {'required': False},
            'password': {'write_only': True},
            'password_repeat': {'write_only': True}
        }

    def create(self, validated_data):
        password = self.initial_data.get('password', 1)
        password_repeat = self.initial_data.get('password_repeat', 2)

        if password_repeat != password:
            error_dict = {
                'password': ['the password and the repeat password must match.']
            }
            raise rest_framework.serializers.ValidationError(
                detail=error_dict
            )

        try:
            validate_password(password=password)
        except django_exceptions.ValidationError as error:
            error_dict = {'password': error.messages}
            raise serializers.ValidationError(detail=error_dict)

        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])

        if user.role == 'admin':
            user.is_staff = True
        user.save()

        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
