import requests

from config import settings
from users.models import User


def check_habit_reward(habit):
    """Корректировка сообщения под вознаграждение"""
    if habit.reward is not None:
        return f'\nА после {habit.reward}.'
    elif habit.linked:
        return f'\nА после {habit.linked.action} {habit.linked.length} секунд.'
    else:
        return ''


def get_tg_data():
    """Получает информацю от API Telegram о новом сообщении в Telegram Bot"""
    result = requests.get(url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/getUpdates').json()
    return result


def check_register_chat_id(tg_data):
    """Проверка пользователя на наличие chat_id"""
    for mes in tg_data['result']:
        if mes['message']['text'] == "/start":
            user = User.objects.get(tg_username=mes['message']['chat']['username'])
            if user is None:
                requests.post(url=f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage',
                              data={'chat_id': mes['message']['chat']['id'],
                                    'text': 'Зарегестрируйся или внеси действующий Телеграмм Ник'})
            else:
                if user.tg_chat_id is None or user.tg_chat_id != mes['message']['chat']['id']:
                    user.tg_chat_id = mes['message']['chat']['id']
                    user.save()
