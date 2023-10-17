from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(email='test1@mail.com', tg_username='drkenni')
        self.user1.set_password('qwer1234')
        self.user2 = User.objects.create_user(email='test2@mail.com', tg_username='drkenni')
        self.user1.set_password('qwer1234')

        self.pleasant_habit = Habit.objects.create(place='место 1',
                                                   time='12:00',
                                                   action='действие 1',
                                                   length=100,
                                                   owner=self.user1)

        self.pleasant_habit_public = Habit.objects.create(place='место 2',
                                                          time='12:00',
                                                          action='действие 2',
                                                          length=100,
                                                          is_published=True,
                                                          owner=self.user1)

        self.unpleasant_habit = Habit.objects.create(place='место 1',
                                                     time='12:00',
                                                     action='действие 3',
                                                     length=100,
                                                     reward='TestReward',
                                                     period=3,
                                                     owner=self.user1)

        self.unpleasant_habit_public = Habit.objects.create(place='место 2',
                                                            time='12:00',
                                                            action='действие 4',
                                                            length=100,
                                                            linked=1,
                                                            period=3,
                                                            is_published=True,
                                                            owner=self.user1)


