from django.contrib import admin

from reviews.models import User


class UserAdmin(admin.ModelAdmin):
    """Кастомная админка для модели пользователя."""
    list_display = (
        'id',
        'username',
        'first_name',
        'email',
        'role',
        'bio',
    )
    list_editable = ('role',)
    search_fields = ('username', 'role')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
