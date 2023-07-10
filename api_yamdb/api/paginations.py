from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    """Паджинация пользавателей."""
    page_size = 10
