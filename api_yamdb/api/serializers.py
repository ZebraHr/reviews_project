import uuid

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

<<<<<<< HEAD
from api.errors import ErrorResponse
from api_yamdb.settings import CHOICES
from reviews.models import User
=======
from reviews.models import Comment, Review
from api_yamdb.api.models import User
from api_yamdb.settings import STATUS
>>>>>>> 39850f021c94c8758ce6c8fe7e28f20afc367457


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'review', 'author', 'text', 'pub_date')
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Вами уже был написан отзыв на это произведение'
            )
        ]

 
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
