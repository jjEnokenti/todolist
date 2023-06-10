from django.urls import path

from .views import category


urlpatterns = [
    path('goal_category/create', category.GoalCategoryCreateView.as_view()),
]
