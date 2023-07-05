from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review
from api_yamdb.api.models import User
from api_yamdb.settings import STATUS


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
    """Сериализует данные модели User."""
    role = serializers.ChoiceField(choices=STATUS, default='user')

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'role')
        model = User
