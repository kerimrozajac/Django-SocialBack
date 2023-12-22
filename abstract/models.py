from django.db import models
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            validated_uuid = uuid.UUID(public_id, version=4)
            return self.get(public_id=validated_uuid)
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404(f"{self.model.__name__} with public_id '{public_id}' not found")


class AbstractModel(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    objects = AbstractManager()

    class Meta:
        abstract = True
