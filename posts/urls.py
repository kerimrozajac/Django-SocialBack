# posts/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from posts.views import UserViewSet, PostViewSet
from comments.views import CommentViewSet

router = SimpleRouter()


router.register("users", UserViewSet, basename="users")
router.register(r"", PostViewSet, basename="posts")

posts_router = routers.NestedSimpleRouter(router, r"", lookup="post")
posts_router.register(r'comment', CommentViewSet, basename="post-comment")

urlpatterns = [
*router.urls,
*posts_router.urls,
path('users/<int:id>/posts/', PostViewSet.as_view({'get': 'list'}), name='user-posts'),
]
