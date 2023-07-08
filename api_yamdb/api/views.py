from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Genre, Category
from .permissions import IsAmdinOrReadOnly
from .serializers import (TitleSerializer,
                          GenreSerializer,
                          CategorySerializer)
from api.filters import TitleFilter


class CreateListDestroyMixin(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    pass


class GenreViewSet(CreateListDestroyMixin):
    """Вьюсет для создания, просмотра и удаления групп."""
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    permission_classes = (IsAmdinOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания, просмотра, изменения и удаления произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filterset_class = TitleFilter
    permission_classes = (IsAmdinOrReadOnly, )
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyMixin):
    """Вьюсет для создания, просмотра и удаления категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAmdinOrReadOnly, )
