from django.urls import path

from .views import (
    UserChangePasswordView,
    UserCreateView,
    UserLoginView,
    UserProfileView,
)


urlpatterns = [
    path('signup', UserCreateView.as_view(), name='user_register'),
    path('login', UserLoginView.as_view(), name='user_login'),
    path('profile', UserProfileView.as_view(), name='user_profile'),
    path('update_password', UserChangePasswordView.as_view(), name='update_password'),
]
