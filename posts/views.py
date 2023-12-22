# posts/views.py
from django.contrib.auth import get_user_model
from rest_framework import viewsets  # new
from rest_framework.permissions import IsAdminUser

from .serializers import PostSerializer
from .models import Post


from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, UserSerializer
from abstract.views import AbstractViewSet


class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get')
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    #def create(self, request, *args, **kwargs):
    #    serializer = self.get_serializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    self.perform_create(serializer)
    #    return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(AbstractViewSet):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        obj = get_user_model().objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
