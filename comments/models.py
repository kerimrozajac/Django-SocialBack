from django.db import models
from abstract.models import AbstractModel, AbstractManager


class CommentManager(AbstractManager):
    pass


class Comment(AbstractModel):
    post = models.ForeignKey("posts.Post", on_delete=models.PROTECT)
    author = models.ForeignKey("accounts.CustomUser", on_delete=models.PROTECT)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    objects = CommentManager()

    def __str__(self):
        return self.author.username
