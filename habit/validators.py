from rest_framework.serializers import ValidationError


def validate_habit_length(value):
    if value > 120:
        raise ValidationError("Время привычки не может превышать 120 секунд.")
    return value


