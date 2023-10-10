from django.urls import path

from habit.apps import HabitConfig
from habit.views import HabitPublishedListAPIView, HabitListAPIView, HabitCreateAPIView, HabitDetailAPIView, \
    HabitDeleteAPIView, HabitUpdateAPIView

app_name = HabitConfig.name

urlpatterns = [
    # Habit
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('', HabitListAPIView.as_view(), name='habit_list'),
    path('public/', HabitPublishedListAPIView.as_view(), name='habit_public_list'),
    path('<int:pk>/', HabitDetailAPIView.as_view(), name='habit_detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habit_delete')
]
