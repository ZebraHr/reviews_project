import uuid
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from api.serializers import (ReviewSerializer,
                             CommentSerializer,
                             UserSerializer,
                             GetTokenSerializer,
                             ProfileSerializer,
                             SignUpSerializer,
                             ProfileSerializer,
                             TitleSerializer,
                             GenreSerializer,
                             CategorySerializer,
                             TitleReadOnlySerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL, DEFAULT_EMAIL_SUBJECT
from reviews.models import User, Title, Genre, Category, Review
from api.permission import (IsAdmin,
                            IsAmdinOrReadOnly,
                            IsAdminModeratorOwnerOrReadOnly)
from api.paginations import ReviewPagination, CommentPagination
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
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
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")).order_by("name")
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filterset_class = TitleFilter
    permission_classes = (IsAmdinOrReadOnly, )
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadOnlySerializer
        return TitleSerializer


class CategoryViewSet(CreateListDestroyMixin):
    """Вьюсет для создания, просмотра и удаления категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAmdinOrReadOnly, )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки отзывов к произведениям"""
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]
    pagination_class = CommentPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки комментариев к отзывам"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]
    pagination_class = ReviewPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class UserViewSet(ModelViewSet):
    """Вьюсет для модели пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'email')

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=ProfileSerializer
    )
    def set_profile(self, request, id=None):
        """Изменяет данные в профайле пользователя."""
        user = get_object_or_404(User, id=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    """Регистрирует пользователя и отправляет код подтверждения."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = str(uuid.uuid4())
    user, created = User.objects.get_or_create(
        **serializer.validated_data,
        confirmation_code=confirmation_code
    )
    send_mail(
        subject=DEFAULT_EMAIL_SUBJECT,
        message=user.confirmation_code,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(user.email,)
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    """"Выдает токен для авторизации."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    return Response({'token': str(AccessToken.for_user(user))},
                    status=status.HTTP_200_OK)
