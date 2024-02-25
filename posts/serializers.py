# posts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from abstract.serializers import AbstractSerializer

from .models import Post
from accounts.models import CustomUser


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='public_id')

    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_liked(self, instance):
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False
        return request.user.has_liked(instance)

    def get_likes_count(self, instance):
        return instance.liked_by.count()

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = str(rep['author'])
        author_public_id = rep["author"]
        author = CustomUser.objects.get_object_by_public_id(author_public_id)
        rep["author"] = UserSerializer(author).data
        return rep

    class Meta:
        fields = (
            "author",
            "title",
            "body",
            "edited",
            "liked",
            "likes_count",
            "created",
            "updated",
            "public_id",
        )
        model = Post
        read_only_fields = ["edited"]


class UserSerializer(AbstractSerializer):  # new

    class Meta:
        model = get_user_model()
        fields = ("username", "public_id", "first_name", "last_name", "email", "is_active", "created", "updated",)
        read_only_field = ["is_active"]
        # nedostaju u modelu: "bio", "avatar" dodati naknadno
