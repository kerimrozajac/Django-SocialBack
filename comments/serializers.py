from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from abstract.serializers import AbstractSerializer
from accounts.models import CustomUser
from posts.serializers import UserSerializer
from comments.models import Comment
from posts.models import Post
from django.contrib.auth import get_user_model


class CommentUserSerializer(AbstractSerializer):  # new

    class Meta:
        model = get_user_model()
        fields = ("username", "public_id",)
        # dodati i avatar u fields


class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='public_id', required=False)
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='public_id', required=False)

    def validate(self, data):
        # Infer the authenticated user as the author if not provided
        # data['author'] = CustomUser.objects.get_object_by_public_id(data.get('author', self.context['request'].user))
        data['author'] = data.get('author', self.context['request'].user)

        # Infer the post from the URL if not provided
        data['post'] = Post.objects.get_object_by_public_id(data.get('post', self.context['view'].kwargs.get('post_pk')))

        return data

    """
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = CustomUser.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data
        return rep
    """

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = CustomUser.objects.get_object_by_public_id(str(rep["author"]))  # Convert UUID to string
        rep["author"] = CommentUserSerializer(author).data
        return rep

    class Meta:
        model = Comment
        # List of all the fields that can be included in a
        # request or a response
        fields = ['id', 'post', 'author', 'body', 'edited', 'created', 'updated', 'public_id']
        # read_only_fields = ["edited"]
        read_only_fields = ["edited", "author", "post"]