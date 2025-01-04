# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Device
from .serializers import DeviceSerializer
from accounts.models import CustomUser  # Adjust according to your project structure
from rest_framework import generics

# Retrieve, Update, and Delete a device
class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'

class DeviceListView(generics.ListAPIView):
    queryset = Device.objects.all()  # Get all devices
    serializer_class = DeviceSerializer  # Use the DeviceSerializer to format the response


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
