from django.contrib import admin

from .models import (
    Comment,
    Goal,
    GoalCategory
)


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
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


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
