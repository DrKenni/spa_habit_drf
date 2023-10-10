from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

from habit.models import Habit
from habit.serializers import HabitSerializer, HabitCreateSerializer


class HabitPublishedListAPIView(ListAPIView):
    """Список публичных привычек"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)


class HabitListAPIView(ListAPIView):
    """Список привычек пользователя"""
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCreateAPIView(CreateAPIView):
    """Создание привычки"""
    serializer_class = HabitCreateSerializer


class HabitDetailAPIView(RetrieveAPIView):
    """Детальный просмотр привычки"""
    serializer_class = HabitCreateSerializer
    queryset = Habit.objects.all()


class HabitDeleteAPIView(DestroyAPIView):
    """Удаление привычки"""
    serializer_class = HabitCreateSerializer


class HabitUpdateAPIView(UpdateAPIView):
    """Обновление привычки"""
    serializer_class = HabitCreateSerializer
    queryset = Habit.objects.all()

