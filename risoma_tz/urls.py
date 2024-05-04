from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API",
        terms_of_service="",
        contact=openapi.Contact(email="aspirpd@gmail.com"),
    ),
    public=True,
    authentication_classes=(SessionAuthentication,),
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blogs.urls', namespace='blogs')),
    path('blogs/api/', include('blogs.api.urls', namespace='blogs-api')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
