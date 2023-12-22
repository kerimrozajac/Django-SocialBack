# posts/views.py
from django.contrib.auth import get_user_model
from rest_framework import viewsets  # new
from rest_framework.permissions import IsAdminUser


from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, UserSerializer
from abstract.views import AbstractViewSet


class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get')
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserViewSet(AbstractViewSet):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        obj = get_user_model().objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
