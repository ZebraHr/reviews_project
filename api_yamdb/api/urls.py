from rest_framework import routers

from api.views import ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register(
    r'title/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
