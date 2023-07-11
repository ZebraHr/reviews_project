from rest_framework.pagination import PageNumberPagination


class TitlesPagination(PageNumberPagination):
    """Паджинация отзывов на произведения."""
    page_size = 5


class OtherPagination(PageNumberPagination):
    """
    Паджинация на прочие ресурсы.
    Жанры, категории, комментарии, отзывы, пользователи.
    """
    page_size = 10
