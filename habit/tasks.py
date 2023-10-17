from datetime import datetime, timedelta

import requests
from celery import shared_task

from config import settings
from habit.models import Habit
from habit.servises import get_tg_data, check_register_chat_id, check_habit_reward


@shared_task
def notice_habit():
    """
    Каждую минуту проверяте на наличие новых пользователей по сообщению в Бот.
    Отправляет уведомления о привычке.
    """
    tg_data = get_tg_data()
    if tg_data['ok'] and tg_data['result'] != []:
        check_register_chat_id(tg_data)
        habits = Habit.objects.filter(is_pleasant=False)
        for habit in habits:
            if datetime.now().time() >= habit.time and datetime.now().date() >= habit.last_time.date():
                send_mes_to_tg.delay(habit.id)
                habit.last_time = datetime.now() + timedelta(days=habit.period)
                habit.save()


@shared_task
def send_mes_to_tg(habit_id):
    """Отправка сообщения"""
    habit = Habit.objects.get(pk=habit_id)
    message = f'Пора начинать {habit.action} за {habit.length} секунд.{check_habit_reward(habit)}'
    requests.post(url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage',
                  data={'chat_id': habit.owner.tg_chat_id, 'text': message})
