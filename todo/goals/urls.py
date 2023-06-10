from django.urls import path

from todo.goals.views import category


urlpatterns = [
    path('goal_category/create', category.GoalCategoryCreateView.as_view()),
]
