import uuid
import datetime as dt
from rest_framework import serializers

from api.errors import ErrorResponse
from api_yamdb.settings import CHOICES
# from django.db.models import Avg
from reviews.models import (Title, Genre,
                            Category, Title,
                            Genre, Category,
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
                'Год не может быть больше текущего')
        return value


# Расчет рейтинга
# rating = serializers.SerializerMethodField()
# def get_rating(self, obj):
#         rating = Review.objects.filter(title=obj).aggregate(
#             Avg('score'))['score__avg']
#         if rating:
#             return int(rating)
#         return None


class CommentSerializer(serializers.ModelSerializer):
    """Комментарии к отзывам на произведения """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'review', 'author', 'text', 'pub_date')
        model = Comment
        read_only_fields = ('review', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    """ Отзывы на произведения """
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError('Проверть оценку произведения')
        
    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'pub_date', 'title', 'score')
        read_only_fields = ('title', 'pub_date')
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
