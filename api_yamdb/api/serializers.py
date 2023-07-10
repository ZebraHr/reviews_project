import uuid

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.errors import ErrorResponse
from api_yamdb.settings import CHOICES, ME
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели юзера."""
    role = serializers.ChoiceField(choices=CHOICES, default='user')
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=ErrorResponse.USERNAME_EXISTS
            )]
    )
    email = serializers.CharField(
        max_length=254,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=ErrorResponse.EMAIL_EXISTS
            )]
    )

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
        """Админ создает валидного юзера и выдает код подтверждения."""
        email = validated_data['email']
        confirmation_code = str(uuid.uuid5(uuid.NAMESPACE_X500, email))
        return User.objects.create(
            **validated_data,
            confirmation_code=confirmation_code
        )


class ProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
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

    @staticmethod
    def validate_username(username):
        if username.lower() == ME:
            raise serializers.ValidationError(ErrorResponse.FORBIDDEN_NAME)
        return username


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError(ErrorResponse.MISSING_USERNAME)
        if confirmation_code is None:
            raise serializers.ValidationError(ErrorResponse.MISSING_CODE)
        return data
