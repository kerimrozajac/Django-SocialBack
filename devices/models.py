# devices/models.py
from django.conf import settings
from django.db import models
from abstract.models import AbstractModel  # Assuming AbstractModel is the same in both apps
from accounts.models import CustomUser 

class Device(AbstractModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, related_name='devices', on_delete=models.CASCADE)
    uid = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField()
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.uid} - {self.ip_address}"
