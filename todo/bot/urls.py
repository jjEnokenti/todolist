from django.urls import path

from . import views


urlpatterns = [
    path('verify', views.BotVerify.as_view()),
]
