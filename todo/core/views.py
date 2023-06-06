from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import UserCreateSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User
