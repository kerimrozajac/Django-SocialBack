# models.py
from django.db import models
from accounts.models import CustomUser  # Adjust the import according to your project structure

class Device(models.Model):
    user = models.ForeignKey(CustomUser, related_name='devices', on_delete=models.CASCADE)
    uid = models.CharField(max_length=255)  # Bluetooth UID
    ip_address = models.GenericIPAddressField()  # Store the device IP address
    is_online = models.BooleanField(default=True)  # Online status
    # Automatically generated ID by Django (Primary key is auto-created by default)
    
    def __str__(self):
        return f"{self.user.username} - {self.uid}"
