
from django.urls import path

from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig

app_name = UsersConfig.name

router = DefaultRouter()
# router.register(r'...', ...ViewSet, basename='...')

urlpatterns = [

] + router.urls
