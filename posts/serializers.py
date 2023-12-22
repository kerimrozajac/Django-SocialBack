# posts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from abstract.serializers import AbstractSerializer

from .models import Post
from accounts.models import CustomUser


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='public_id')

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")

        return value

    class Meta:
        fields = (
            "id",
            "author",
            "title",
            "body",
            "edited",
            "created",
            "updated",
            "public_id",
        )
        model = Post
        read_only_fields = ["edited"]


class UserSerializer(AbstractSerializer): # new

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "public_id", "first_name", "last_name", "email", "is_active", "created", "updated",)
        # umjesto created -> date_joined
        # nedostaju u modelu: "bio", "avatar", "updated" dodati naknadno
