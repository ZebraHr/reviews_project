import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, filters, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.paginations import UserPagination
from api.permissions import IsAdmin
from api.serializers import (GetTokenSerializer, ProfileSerializer,
                             SignUpSerializer, UserSerializer)
from api_yamdb.settings import DEFAULT_EMAIL_SUBJECT, DEFAULT_FROM_EMAIL
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = UserPagination
    http_method_names = ('get', 'post', 'patch', 'delete',)

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
    email = serializer.validated_data['email']
    confirmation_code = str(uuid.uuid5(uuid.NAMESPACE_X500, email))
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
