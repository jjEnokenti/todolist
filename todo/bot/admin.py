from bot.models import TgUser
from django.contrib import admin


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    pass
