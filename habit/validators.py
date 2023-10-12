from rest_framework.serializers import ValidationError


def validate_habit_length(value):
    if value > 120:
        raise ValidationError("Время привычки не может превышать 120 секунд.")
    return value


def validate_habit_period(value):
    if value > 7:
        raise ValidationError("Привычку нельзя выполнять реже 7 дней.")
    return value
