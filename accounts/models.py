# accounts/models.py
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class CustomUserManager(BaseUserManager):

    def get_object_by_public_id(self, public_id):
        try:
            return self.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404("User not found by public_id")


class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=100)
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    objects = CustomUserManager()



