from django.contrib import admin

from .models import (
    Board,
    BoardParticipant,
    Comment,
    Goal,
    GoalCategory,
)


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'user', 'created', 'updated')
    search_fields = ('title', 'created')


class GoalAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'priority',
        'status',
        'due_date',
        'created',
        'updated'
    )
    search_fields = ('title', 'created')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created', 'updated')
    search_fields = ('text', 'created')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted', 'created', 'updated')
    search_fields = ('title', 'created')


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'board', 'role', 'created', 'updated')
    search_fields = ('role', 'created')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
