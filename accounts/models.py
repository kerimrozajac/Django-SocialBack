# accounts/models.py
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from abstract.models import AbstractModel, AbstractManager
from posts.models import Post


class CustomUserManager(BaseUserManager, AbstractManager):
    pass

    #def get_object_by_public_id(self, public_id):
    #    try:
    #        validated_uuid = uuid.UUID(public_id, version=4)
    #        return self.get(public_id=validated_uuid)
    #    except (ObjectDoesNotExist, ValueError, TypeError):
    #        raise Http404("User not found by public_id")


class CustomUser(AbstractUser, AbstractModel, PermissionsMixin):
    posts_liked = models.ManyToManyField("posts.Post", related_name="liked_by")
    # name = models.CharField(null=True, blank=True, max_length=100)
    objects = CustomUserManager()

    def like(self, post):
        """Like `post` if it hasn't been done yet"""
        return self.posts_liked.add(post)

    def remove_like(self, post):
        """Remove a like from a `post`"""
        return self.posts_liked.remove(post)

    def has_liked(self, post):
        """Return True if the user has liked a `post`; else False"""
        return self.posts_liked.filter(pk=post.pk).exists()

