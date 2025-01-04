# devices/serializers.py
from rest_framework import serializers
from abstract.serializers import AbstractSerializer  # Assuming AbstractSerializer is the same for both apps
from .models import Device

class DeviceSerializer(AbstractSerializer):
    class Meta:
        model = Device
        fields = ('uid', 'user', 'ip_address', 'is_online', 'created', 'updated', 'public_id')
        read_only_fields = ['created', 'updated']
