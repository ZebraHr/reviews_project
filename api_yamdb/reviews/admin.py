from django.contrib import admin
from .models import Review, Comment


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


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
