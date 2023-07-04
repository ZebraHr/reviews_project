from django.contrib import admin

from api_yamdb.api.models import User


class UserAdmin(admin.ModelAdmin):
    """Кастомная админка для модели пользователя."""
    list_display = (
        'id',
        'username',
        'first_name',
        'email',
        'role'
    )
    list_editable = ('role',)
    search_fields = ('username', 'role')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
