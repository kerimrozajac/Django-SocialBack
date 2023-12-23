# posts/models.py
from django.conf import settings
from django.db import models

from abstract.models import AbstractModel, AbstractManager


class PostManager(AbstractManager):
    pass


class Post(AbstractModel):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)
    objects = PostManager()

    def __str__(self):
        return f"{self.title}"
