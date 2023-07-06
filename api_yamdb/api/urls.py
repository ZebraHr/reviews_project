from django.urls import include, path
from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from api.views import UserViewSet, get_token, sign_up
=======
from api.views import ReviewViewSet, CommentViewSet
from api_yamdb.api.views import UserViewSet, sign_up, get_token
>>>>>>> 39850f021c94c8758ce6c8fe7e28f20afc367457


v1_router = DefaultRouter()
v1_router.register(
    r'title/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
v1_router.register(
    r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
v1_router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
