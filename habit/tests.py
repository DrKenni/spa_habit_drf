from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from habit.servises import check_habit_reward
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test1@mail.com', tg_username='drkenni')
        self.user.set_password('qwer1234')
        self.second_user = User.objects.create(email='test2@mail.com', )
        self.second_user.set_password('qwer1234')
        self.maxDiff = None

        self.pleasant_habit = Habit.objects.create(place='место 1',
                                                   time='12:00',
                                                   action='действие 1',
                                                   length=100,
                                                   is_pleasant=True,
                                                   owner=self.user)

        self.pleasant_habit_public = Habit.objects.create(place='место 2',
                                                          time='12:00',
                                                          action='действие 2',
                                                          length=100,
                                                          is_public=True,
                                                          is_pleasant=True,
                                                          owner=self.user)

        self.unpleasant_habit = Habit.objects.create(place='место 1',
                                                     time='12:00',
                                                     action='действие 3',
                                                     length=100,
                                                     reward='награда',
                                                     period=3,
                                                     owner=self.user)

        self.unpleasant_habit_public = Habit.objects.create(place='место 2',
                                                            time='12:00',
                                                            action='действие 4',
                                                            length=100,
                                                            linked=self.pleasant_habit,
                                                            period=3,
                                                            is_public=True,
                                                            owner=self.user)

    def test_habit_create(self):
        """
        Создание неприятной привычки
        (условие не выполнено: Нужно заполнить поле tg_username в профиле)
        """
        self.client.force_authenticate(user=self.second_user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'действие4',
                                                                    'time': '21:00',
                                                                    'action': 'место4',
                                                                    'length': 120,
                                                                    'period': 1,
                                                                    'reward': 'награда'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_habit_create(self):
        """
        Создание приятной привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'место 3',
                                                                    'time': '12:00',
                                                                    'action': 'действие 3',
                                                                    'is_pleasant': True,
                                                                    'length': 100, })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_pleasant_habit_create_length(self):
        """
        Создание приятной привычки
        (условие не выполнено: Время привычки не может превышать 120 секунд)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'место',
                                                                    'time': '21:00',
                                                                    'action': 'действие',
                                                                    'is_pleasant': True,
                                                                    'length': 121})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_habit_create_period(self):
        """
        Создание приятной привычки
        (условие не выполнено: У приятной привычки не может быть переодичности)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'действие',
                                                                    'time': '21:00',
                                                                    'action': 'место',
                                                                    'length': 120,
                                                                    'is_pleasant': True,
                                                                    'period': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_habit_create_reward(self):
        """
        Создание неприятной привычки
        (условие не выполнено: У приятной привычки не может быть связанной привычки или вознаграждения)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'действие4',
                                                                    'time': '21:00',
                                                                    'action': 'место4',
                                                                    'length': 120,
                                                                    'period': 1,
                                                                    'is_pleasant': True,
                                                                    'reward': 'награда'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unpleasant_habit_create(self):
        """
        Создание неприятной привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'действие4',
                                                                    'time': '21:00',
                                                                    'action': 'место4',
                                                                    'length': 120,
                                                                    'period': 1,
                                                                    'reward': 'награда'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unpleasant_habit_create_reward(self):
        """
        Создание неприятной привычки
        (условие не выполнено: Нельзя одновременно выбрать приятную привычку и вознаграждение)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'действие4',
                                                                    'time': '21:00',
                                                                    'action': 'место4',
                                                                    'length': 120,
                                                                    'period': 3,
                                                                    'reward': 'награда',
                                                                    'linked': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unpleasant_habit_create_linked(self):
        """
        Создание неприятной привычки
        (условие не выполнено: Связанной привычкой может быть только приятная привычка)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'действие4',
                                                                    'time': '21:00',
                                                                    'action': 'место4',
                                                                    'length': 120,
                                                                    'reward': 'награда',
                                                                    'linked': 4})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unpleasant_habit_create_period(self):
        """
        Создание неприятной привычки
        (условие не выполнено: Привычку нельзя выполнять реже 7 дней)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:habit_create'), {'place': 'действие4',
                                                                    'time': '21:00',
                                                                    'action': 'место4',
                                                                    'length': 120,
                                                                    'period': 8,
                                                                    'reward': 'награда'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_habit_1(self):
        """
        Вывод списка привычек пользователя
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habit:habit_list'))
        self.assertEqual(
            response.json(),
            {'count': 4,
             'next': None,
             'previous': None,
             'results': [
                 {'id': self.pleasant_habit.id,
                  'is_pleasant': 'Приятная привычка',
                  'is_public': 'Не публичная',
                  'owner': 'test1@mail.com',
                  'place': 'место 1',
                  'time': '12:00:00',
                  'action': 'действие 1',
                  'reward': None,
                  'length': 100,
                  'period': None,
                  'last_time': self.pleasant_habit.last_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                  'linked': None},
                 {'id': self.pleasant_habit_public.id,
                  'is_pleasant': 'Приятная привычка',
                  'is_public': 'Публичная',
                  'owner': 'test1@mail.com',
                  'place': 'место 2',
                  'time': '12:00:00',
                  'action': 'действие 2',
                  'reward': None,
                  'length': 100,
                  'period': None,
                  'last_time': self.pleasant_habit_public.last_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                  'linked': None},
                 {'id': self.unpleasant_habit.id,
                  'is_pleasant': 'Неприятная привычка',
                  'is_public': 'Не публичная',
                  'owner': 'test1@mail.com',
                  'place': 'место 1',
                  'time': '12:00:00',
                  'action': 'действие 3',
                  'reward': 'награда',
                  'length': 100,
                  'period': 3,
                  'last_time': self.unpleasant_habit.last_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                  'linked': None},
                 {'id': self.unpleasant_habit_public.id,
                  'is_pleasant': 'Неприятная привычка',
                  'is_public': 'Публичная',
                  'owner': 'test1@mail.com',
                  'place': 'место 2',
                  'time': '12:00:00',
                  'action': 'действие 4',
                  'reward': None,
                  'length': 100,
                  'period': 3,
                  'last_time': self.unpleasant_habit_public.last_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                  'linked': self.pleasant_habit.id}]}
        )

    def test_list_habit_2(self):
        """
        Вывод списка привычек пользователя
        """
        self.client.force_authenticate(user=self.second_user)
        response = self.client.get(reverse('habit:habit_list'))
        self.assertEqual(
            response.json(),
            {'count': 0,
             'next': None,
             'previous': None,
             'results': []})

    def test_public_list_habit(self):
        """
        Вывод списка публичных привычек пользователя
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habit:habit_public_list'))
        self.assertEqual(
            response.json(),
            {'count': 2,
             'next': None,
             'previous': None,
             'results': [
                 {'id': self.pleasant_habit_public.id,
                  'is_pleasant': 'Приятная привычка',
                  'is_public': 'Публичная',
                  'owner': 'test1@mail.com',
                  'place': 'место 2',
                  'time': '12:00:00',
                  'action': 'действие 2',
                  'reward': None,
                  'length': 100,
                  'period': None,
                  'last_time': self.pleasant_habit_public.last_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                  'linked': None},
                 {'id': self.unpleasant_habit_public.id,
                  'is_pleasant': 'Неприятная привычка',
                  'is_public': 'Публичная',
                  'owner': 'test1@mail.com',
                  'place': 'место 2',
                  'time': '12:00:00',
                  'action': 'действие 4',
                  'reward': None,
                  'length': 100,
                  'period': 3,
                  'last_time': self.unpleasant_habit_public.last_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                  'linked': self.pleasant_habit.id}]}
        )

    def test_detail_habit(self):
        """
        Просмотр одной привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habit:habit_detail', kwargs={'pk': self.pleasant_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.pleasant_habit.pk)

    def test_update_habit(self):
        """
        Редактирование привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('habit:habit_update', kwargs={'pk': self.pleasant_habit.pk}),
                                     {'place': 'Новое место'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 'Новое место')

    def test_delete_habit(self):
        """
        Тестирование удаления привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('habit:habit_delete', kwargs={'pk': self.unpleasant_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_habit_linked(self):
        """
        Тестирование удаления привычки
        (условие не выполнено: Это связанная привычка, не могу удалить)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('habit:habit_delete', kwargs={'pk': self.pleasant_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_check_habit_reward(self):
        self.assertEqual(check_habit_reward(self.unpleasant_habit),
                         f'\nА после {self.unpleasant_habit.reward}.')
