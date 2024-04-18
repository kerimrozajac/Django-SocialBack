# accounts/models.py
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.crypto import get_random_string

from abstract.models import AbstractModel, AbstractManager
from posts.models import Post


class CustomUserManager(BaseUserManager, AbstractManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, AbstractModel, PermissionsMixin):
    posts_liked = models.ManyToManyField("posts.Post", related_name="liked_by")
    verification_code = models.CharField(max_length=5, blank=True)
    # name = models.CharField(null=True, blank=True, max_length=100)
    objects = CustomUserManager()

    def generate_verification_code(self):
        # Generate a random 5-character verification code
        self.verification_code = get_random_string(length=5)

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.generate_verification_code()
        super().save(*args, **kwargs)

    def like(self, post):
        """Like `post` if it hasn't been done yet"""
        return self.posts_liked.add(post)

    def remove_like(self, post):
        """Remove a like from a `post`"""
        return self.posts_liked.remove(post)

    def has_liked(self, post):
        """Return True if the user has liked a `post`; else False"""
        return self.posts_liked.filter(pk=post.pk).exists()

