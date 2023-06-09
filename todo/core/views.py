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

from .serializers import (
    UserChangePasswordSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request):
        logout(request=request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
