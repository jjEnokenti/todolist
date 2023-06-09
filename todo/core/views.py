from django.contrib.auth import (
    login,
    logout
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import (
    generics,
    status
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserChangePasswordSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer
)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserRetrieveSerializer

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = UserUpdateSerializer

        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.serializer_class = UserUpdateSerializer

        return super().patch(request, *args, **kwargs)

    def delete(self, request):
        logout(request=request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    queryset = User

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
