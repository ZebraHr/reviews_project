from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from api_yamdb.api.models import User
from api_yamdb.api.permission import IsAdmin
from api_yamdb.api.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """Вьюсет для пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


def sign_up():
    """Регистрация."""
    pass


def get_token():
    """Получение токена."""
    pass
