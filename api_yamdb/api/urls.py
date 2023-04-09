from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.v1.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewsViewSet,
    CommentViewSet,
    get_token,
    sign_up,
    UsersViewSet,
)


router_v1 = DefaultRouter()

router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/test/', include('djoser.urls')),
    path('v1/auth/test/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
