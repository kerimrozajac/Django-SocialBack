# django_project/urls.py
from django.contrib import admin
from django.urls import path, include  # new
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView,)
from posts.views import PostViewSet
from accounts.views import RegisterView, VerifyCodeView

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
]