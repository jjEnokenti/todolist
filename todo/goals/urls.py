from django.urls import path

from .views import (
    category,
    comment,
    goal
)


urlpatterns = [
    # goal categories
    path('goal_category/create', category.GoalCategoryCreateView.as_view()),
    path('goal_category/list', category.GoalCategoryListView.as_view()),
    path('goal_category/<int:pk>', category.GoalCategoryView.as_view()),

    # goals
    path('goal/list', goal.GoalListView.as_view()),
    path('goal/create', goal.GoalCreateView.as_view()),
    path('goal/<int:pk>', goal.GoalView.as_view()),

    # comments
    path('goal_comment/list', comment.CommentListView.as_view()),
    path('goal_comment/create', comment.CommentCreateView.as_view()),
    path('goal_comment/<int:pk>', comment.CommentView.as_view()),
]
