from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
# from django.db.models import Avg
from reviews.models import Comment, Review
from api_yamdb.api.models import User
from api_yamdb.settings import STATUS

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
        return value

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
