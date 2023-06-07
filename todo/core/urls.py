from django.urls import path

from .views import (
    UserCreateView,
    UserLoginView,
    UserRetrieveUpdateView
)


urlpatterns = [
    path('signup', UserCreateView.as_view()),
    path('login', UserLoginView.as_view()),
    path('profile', UserRetrieveUpdateView.as_view()),
]
