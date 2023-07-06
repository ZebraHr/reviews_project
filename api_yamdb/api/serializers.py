import uuid

from rest_framework import serializers

from api.errors import ErrorResponse
from api_yamdb.settings import CHOICES
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели юзера."""
    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio',
        )
        model = User

    def create(self, validated_data):
        """Создает валидного юзера и выдает код подтверждения."""
        confirmation_code = str(uuid.uuid4())
        return User.objects.create(
            **validated_data,
            confirmation_code=confirmation_code
        )

    @staticmethod
    def validate_username(username):
        if username.lower() == 'me':
            raise serializers.ValidationError(ErrorResponse.FORBIDDEN_NAME)
        return username


class ProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=150)

    def validate(self, data):
        username = data.get('username')
        UserSerializer.validate_username(username)
        email = data.get('email')
        if username is None:
            raise serializers.ValidationError(ErrorResponse.MISSING_USERNAME)
        if email is None:
            raise serializers.ValidationError(ErrorResponse.MISSING_EMAIL)
        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(ErrorResponse.USERNAME_EXISTS)
        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(ErrorResponse.EMAIL_EXISTS)
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError(ErrorResponse.MISSING_USERNAME)
        if confirmation_code is None:
            raise serializers.ValidationError(ErrorResponse.MISSING_CODE)
        return data
