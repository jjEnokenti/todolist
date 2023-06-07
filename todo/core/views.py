from django.contrib.auth import login
from rest_framework import generics
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer
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
