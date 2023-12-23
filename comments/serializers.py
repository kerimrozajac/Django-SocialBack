from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from abstract.serializers import AbstractSerializer
from accounts.models import CustomUser
from posts.serializers import UserSerializer
from comments.models import Comment
from posts.models import Post


class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='public_id')
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='public_id')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = CustomUser.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data
        return rep

    class Meta:
        model = Comment
        # List of all the fields that can be included in a
        # request or a response
        fields = ['id', 'post', 'author', 'body', 'edited', 'created', 'updated', 'public_id']
        read_only_fields = ["edited"]
