# posts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from abstract.serializers import AbstractSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "author",
            "title",
            "body",
            "created_at",
        )
        model = Post


class UserSerializer(AbstractSerializer): # new

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "public_id", "first_name", "last_name", "email", "is_active", "created", "updated",)
        # umjesto created -> date_joined
        # nedostaju u modelu: "bio", "avatar", "updated" dodati naknadno
