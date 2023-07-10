from rest_framework.pagination import PageNumberPagination


class ReviewPagination(PageNumberPagination):
    """Паджинация отзывов на произведения"""
    page_size = 5


class CommentPagination(PageNumberPagination):
    """Паджинация комментариев к отзывам"""
    page_size = 15

class UserPagination(PageNumberPagination):
    """Паджинация пользавателей."""
    page_size = 10
