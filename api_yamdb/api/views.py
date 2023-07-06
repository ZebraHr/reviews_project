from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from .serializers import (ReviewSerializer, CommentSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .paginations import ReviewPagination, CommentPagination
from django_filters.rest_framework import DjangoFilterBackend


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки отзывов к произведениям"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = CommentPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filters_field = ('author', )
    search_fields = ('author', )
    ordering_fields = ('pub_date', )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки комментариев к отзывам"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = ReviewPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter)
    filters_field = ('score',)
    search_fields = ('score', 'author', 'title')
    ordering_fields = ('pub_date', 'score')

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
