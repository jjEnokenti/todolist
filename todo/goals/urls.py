from django.urls import path

from .views import (
    board,
    category,
    comment,
    goal,
)


urlpatterns = [
    # goal categories
    path(
        'goal_category/create',
        category.GoalCategoryCreateView.as_view(),
        name='create_goal_category'
    ),
    path(
        'goal_category/list',
        category.GoalCategoryListView.as_view(),
        name='list_goal_category'
    ),
    path(
        'goal_category/<int:pk>',
        category.GoalCategoryView.as_view(),
        name='detail_goal_category'
    ),

    # goals
    path(
        'goal/list',
        goal.GoalListView.as_view(),
        name='list_goal'
    ),
    path(
        'goal/create',
        goal.GoalCreateView.as_view(),
        name='create_goal'
    ),
    path(
        'goal/<int:pk>',
        goal.GoalView.as_view(),
        name='detail_goal'
    ),

    # comments
    path(
        'goal_comment/list',
        comment.CommentListView.as_view(),
        name='list_goal_comment'
    ),
    path(
        'goal_comment/create',
        comment.CommentCreateView.as_view(),
        name='create_goal_comment'
    ),
    path(
        'goal_comment/<int:pk>',
        comment.CommentView.as_view(),
        name='detail_goal_comment'
    ),

    # boards
    path(
        'board/list',
        board.BoardListView.as_view(),
        name='list_board'
    ),
    path(
        'board/create',
        board.BoardCreateView.as_view(),
        name='create_board'
    ),
    path(
        'board/<int:pk>',
        board.BoardView.as_view(),
        name='detail_board'
    ),
]
