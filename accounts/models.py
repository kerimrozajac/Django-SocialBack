# accounts/models.py
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from abstract.models import AbstractModel, AbstractManager


class CustomUserManager(BaseUserManager, AbstractManager):
    pass

    #def get_object_by_public_id(self, public_id):
    #    try:
    #        validated_uuid = uuid.UUID(public_id, version=4)
    #        return self.get(public_id=validated_uuid)
    #    except (ObjectDoesNotExist, ValueError, TypeError):
    #        raise Http404("User not found by public_id")


class CustomUser(AbstractUser, AbstractModel, PermissionsMixin):
    #name = models.CharField(null=True, blank=True, max_length=100)
    objects = CustomUserManager()



