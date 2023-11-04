from datetime import datetime

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.permissions import IsOwner
from habit.serializers import HabitSerializer, HabitCreateUpdateSerializer

from users.models import User

# Контроллеры Habit


class HabitPublishedListAPIView(ListAPIView):
    """Список публичных привычек"""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]
    queryset = Habit.objects.filter(is_public=True)


class HabitListAPIView(ListAPIView):
    """Список привычек пользователя"""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitCreateAPIView(CreateAPIView):
    """Создание привычки"""
    serializer_class = HabitCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.last_time = datetime.now()
        new_habit.save()

    def get(self, request):
        users = User.objects.all()
        serializer = HabitCreateUpdateSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)


class HabitDetailAPIView(RetrieveAPIView):
    """Детальный просмотр привычки"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    queryset = Habit.objects.all()


class HabitDeleteAPIView(DestroyAPIView):
    """Удаление привычки"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Habit.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if len(Habit.objects.filter(linked=instance)) > 0:
            return Response({'error_message': 'Это связанная привычка, не могу удалить'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class HabitUpdateAPIView(UpdateAPIView):
    """Обновление привычки"""
    serializer_class = HabitCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Habit.objects.all()

    def perform_update(self, serializer):
        update_habit = serializer.save()
        update_habit.save()
