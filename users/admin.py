from django.contrib import admin

from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'tg_chat_id', 'is_staff', 'is_active', 'is_superuser')
