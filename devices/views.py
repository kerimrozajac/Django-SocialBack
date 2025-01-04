# devices/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from abstract.views import AbstractViewSet
from .models import Device
from .serializers import DeviceSerializer
from rest_framework.views import APIView 
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser  # Ensure CustomUser is imported


class DeviceDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_object(self, user_id, device_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            device = Device.objects.get(id=device_id, user=user)
            return device
        except CustomUser.DoesNotExist:
            return None
        except Device.DoesNotExist:
            return None

    def get(self, request, id, device_id):
        device = self.get_object(id, device_id)
        if device is None:
            return Response({'error': 'Device or user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def put(self, request, id, device_id):
        device = self.get_object(id, device_id)
        if device is None:
            return Response({'error': 'Device or user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DeviceSerializer(device, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, device_id):
        device = self.get_object(id, device_id)
        if device is None:
            return Response({'error': 'Device or user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Ensures the user is authenticated
    serializer_class = DeviceSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']  # Fetch the user ID from the URL
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Device.objects.none()  # Return empty queryset if user doesn't exist
        return Device.objects.filter(user=user)

class DeviceViewSet(AbstractViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    
    def get_queryset(self):
        return Device.objects.all()

    def get_object(self):
        # Ensure the get_object_by_public_id method exists, or change to get by pk
        try:
            obj = Device.objects.get(id=self.kwargs['pk'])
        except Device.DoesNotExist:
            raise NotFound("Device not found")
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def set_online(self, request, *args, **kwargs):
        device = self.get_object()
        device.is_online = True
        device.save()
        return Response({'status': 'device set online'})

    @action(methods=['post'], detail=True)
    def set_offline(self, request, *args, **kwargs):
        device = self.get_object()
        device.is_online = False
        device.save()
        return Response({'status': 'device set offline'})


class RegisterDeviceView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        uid = request.data.get('uid')
        ip_address = request.data.get('ip_address')
        
        # Validate that the user exists
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new device entry
        device = Device.objects.create(
            user=user,
            uid=uid,
            ip_address=ip_address,
            is_online=True
        )
        
        # Serialize and return the created device data
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
