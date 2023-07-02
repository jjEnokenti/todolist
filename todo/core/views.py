from django.contrib.auth import (
    login,
    logout,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_spectacular.utils import extend_schema
from rest_framework import (
    generics,
    status,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    UserChangePasswordSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
)


@extend_schema(
    tags=['auth'],
    description='Register new user method',
    summary='register new user'
)
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    @extend_schema(
        tags=['auth'],
        description='User login method',
        summary='authenticate user'
    )
    def post(self, request, *args, **kwargs):
        """POST method handler."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


@method_decorator(ensure_csrf_cookie, name='dispatch')
@extend_schema(
    tags=['profile'],
)
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    @extend_schema(
        tags=['profile'],
        description='User logout',
        summary='user logout'
    )
    def delete(self, request, *args, **kwargs):
        logout(request=request)

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['profile'],
    description='User profile change password method',
    summary='profile password change'
)
class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
