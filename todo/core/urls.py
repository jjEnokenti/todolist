from django.urls import path

from .views import UserCreateView


urlpatterns = [
    path('core/signup', UserCreateView.as_view())
]
