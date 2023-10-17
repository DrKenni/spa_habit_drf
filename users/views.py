from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from habit.permissions import IsModerator, IsOwner
from users.models import User
from users.serializers import UserSerializer

# Контроллеры User


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""
    serializer_class = UserSerializer


class UserListAPIView(ListAPIView):
    """Список пользователей"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | IsModerator]
    queryset = User.objects.all()


class UserDetailAPIView(RetrieveAPIView):
    """Детальный просмотр пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | IsOwner]
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """Обновление пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | IsOwner]
    queryset = User.objects.all()


class UserDeleteAPIView(DestroyAPIView):
    """Удаление пользователея"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated | IsOwner]
