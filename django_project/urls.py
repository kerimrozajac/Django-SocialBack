# django_project/urls.py
from django.contrib import admin
from django.urls import path, include  # new
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView,)
from posts.views import PostViewSet
from accounts.views import RegisterView, VerifyCodeView
from devices.views import RegisterDeviceView, DeviceListView, DeviceDetailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("posts.urls")),
    #path('api/v1/<str:public_id>/', PostViewSet.as_view({'put': 'update'}), name='post-detail'),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    #path("api/v1/auth/register/", include("dj_rest_auth.registration.urls")),
    #path("api/v1/auth/register/", CustomRegisterView.as_view(), name="custom_register"),
    path("api/v1/auth/register/", RegisterView.as_view(), name="register"),
    path("api/v1/auth/verify-code/", VerifyCodeView.as_view(), name="verify_code"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('api/register_device/', RegisterDeviceView.as_view(), name='register_device'),
    path('api/devices/', DeviceListView.as_view(), name='device_list'),  # New route for listing devices
    path('api/device/<int:id>/', DeviceDetailView.as_view(), name='device_detail'),  # Get, Update, or Delete a device


]