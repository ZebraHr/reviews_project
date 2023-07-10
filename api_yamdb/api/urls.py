from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.views import (UserViewSet,
                       get_token,
                       sign_up,
                       ReviewViewSet,
                       CommentViewSet)


from .views import (TitleViewSet,
                    CategoryViewSet,
                    GenreViewSet)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
