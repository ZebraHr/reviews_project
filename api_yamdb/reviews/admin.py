from django.contrib import admin

<<<<<<< HEAD
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
=======
from .models import Review, Comment, Title, Category, Genre


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date',)
    empty_value_display = '-пусто-'
    search_fields = ('text',)
    list_filter = ('pub_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author', 'pub_date',)
    list_filter = ('pub_date',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year',
                    'rating', 'genre', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)

>>>>>>> 39850f021c94c8758ce6c8fe7e28f20afc367457
