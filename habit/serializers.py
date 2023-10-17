from rest_framework import serializers

from habit.models import Habit
from habit.validators import validate_habit_period, validate_habit_length
from users.models import User
from users.serializers import UserSerializer


class HabitSerializer(serializers.ModelSerializer):
    is_pleasant = serializers.SerializerMethodField()
    is_public = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_is_pleasant(self, habit):
        if habit.is_pleasant:
            return "Приятная привычка"
        else:
            return "Неприятная привычка"

    def get_is_public(self, habit):
        if habit.is_public:
            return "Публичная"
        else:
            return "Не публичная"

    def get_owner(self, habit):
        return habit.owner.email

    class Meta:
        model = Habit
        fields = '__all__'


class HabitCreateUpdateSerializer(serializers.ModelSerializer):
    length = serializers.IntegerField(validators=[validate_habit_length])
    period = serializers.IntegerField(validators=[validate_habit_period])

    def validate(self, attrs):
        if attrs:
            owner_id = self.context.get('request').user.id
            owner = User.objects.filter(id=owner_id).first()
            if owner.tg_username is None:
                raise serializers.ValidationError(f"Чтобы создать привычку, нужно заполнить поле tg_username в профиле."
                                                  f"Узнать его можно в Telegram -> Настройки -> Имя позьзователя")

        if attrs.get('is_pleasant'):
            if attrs.get('reward') or attrs.get('linked'):
                raise serializers.ValidationError("У приятной привычки не может быть "
                                                  "связанной привычки или вознаграждения")
            if attrs.get('period'):
                raise serializers.ValidationError("У приятной привычки не может быть переодичности, "
                                                  "она выполняется после связанной привычки")

        if attrs.get('reward') and attrs.get('linked'):
            raise serializers.ValidationError("Нельзя одновременно выбрать приятную привычку и вознаграждение")

        if 'linked' in attrs:
            habit_id = attrs.get('linked').id
            habit = Habit.objects.filter(id=habit_id).first()
            if habit.is_pleasant is False:
                raise serializers.ValidationError("Связаной привычкой может быть только приятная привычка")

        return attrs

    class Meta:
        model = Habit
        fields = '__all__'
