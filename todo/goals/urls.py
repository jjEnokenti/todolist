from django.urls import path

from .views import (
    category,
    goal
)


urlpatterns = [
    # goal category
    path('goal_category/create', category.GoalCategoryCreateView.as_view()),
    path('goal_category/list', category.GoalCategoryListView.as_view()),
    path('goal_category/<int:pk>', category.GoalCategoryManageView.as_view()),

    # goal
    path('goal/list', goal.GoalListView.as_view()),
    path('goal/create', goal.GoalCreateView.as_view()),
]
