from django.contrib import admin

from .models import GoalCategory


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'created')


admin.site.register(GoalCategory, GoalCategoryAdmin)
