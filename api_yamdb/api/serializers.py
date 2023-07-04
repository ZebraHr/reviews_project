from rest_framework import serializers

from api_yamdb.api.models import STATUS, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализует данные модели User."""
    role = serializers.ChoiceField(choices=STATUS, default='user')

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'role')
        model = User
