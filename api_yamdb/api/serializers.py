import uuid
import datetime as dt

from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from api.errors import ErrorResponse
from api_yamdb.settings import CHOICES, ME
from api_yamdb.settings import CHOICES
from reviews.models import (Title, Genre,
                            Category,
                            Review, User,
                            Comment)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализует данные модели Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализует данные модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализует данные модели Title."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                ErrorResponse.YEAR_TILL_NOW
            )
        return value


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """Сериализует вывод произведения с расчитанным рейтингом."""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Комментарии к отзывам на произведения."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Отзывы на произведения."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        request = self.context['request']
        title = get_object_or_404(
            Title,
            id=self.context['view'].kwargs.get('title_id'))
        if request.method == 'POST':
            if Review.objects.filter(title=title,
                                     author=request.user).exists():
                raise ValidationError(
                    ErrorResponse.ONE_REVIEW_ONLY
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


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
    """Сериализатор профиля."""
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации."""
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

    def validate_username(self, username):
        if username.lower() == ME:
            raise serializers.ValidationError(ErrorResponse.FORBIDDEN_NAME)
        return username


class GetTokenSerializer(serializers.Serializer):
    """"Сериализатор получения токена."""
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
