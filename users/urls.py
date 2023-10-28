from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserUpdateAPIView, UserDeleteAPIView, UserDetailAPIView

app_name = UsersConfig.name

urlpatterns = [
    # User
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('view/<int:pk>/', UserDetailAPIView.as_view(), name='user_view'),
    path('edit/<int:pk>/', UserUpdateAPIView.as_view(), name='user_edit'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user_delete'),

    # Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
