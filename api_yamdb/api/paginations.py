from rest_framework.pagination import PageNumberPagination


class ReviewPagination(PageNumberPagination):
    page_size = 5


class CommentPagination(PageNumberPagination):
    page_size = 15