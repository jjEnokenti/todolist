from django.urls import path

from .views import (
    UserChangePasswordView,
    UserCreateView,
    UserLoginView,
    UserProfileView
)


urlpatterns = [
    path('signup', UserCreateView.as_view()),
    path('login', UserLoginView.as_view()),
    path('profile', UserProfileView.as_view()),
    path('update_password', UserChangePasswordView.as_view()),
]
