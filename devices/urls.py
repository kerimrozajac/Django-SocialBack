# devices/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, DeviceListView, DeviceDetailView

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:id>/devices/', DeviceListView.as_view(), name='user-devices-list'),
    path('users/<int:id>/devices/<int:device_id>/', DeviceDetailView.as_view(), name='device-detail'),

]