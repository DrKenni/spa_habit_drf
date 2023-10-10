from rest_framework import serializers

from habit.models import Habit
from habit.validators import validate_habit_period, validate_habit_reward


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'


class HabitCreateSerializer(serializers.ModelSerializer):
    length = serializers.IntegerField(validators=[validate_habit_period])
    # reward = serializers.CharField(validators=[validate_habit_reward])
    # linked = проверка на вознаграждение

    class Meta:
        model = Habit
        fields = '__all__'
