from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api_yamdb.api.views import UserViewSet, sign_up, get_token

router = DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
