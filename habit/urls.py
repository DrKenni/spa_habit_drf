
from django.urls import path

from rest_framework.routers import DefaultRouter

from habit.apps import HabitConfig

app_name = HabitConfig.name

router = DefaultRouter()
# router.register(r'...', ...ViewSet, basename='...')

urlpatterns = [

] + router.urls
