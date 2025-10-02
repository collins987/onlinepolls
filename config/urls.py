from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from polls.views import landing

schema_view = get_schema_view(
    openapi.Info(
        title="Online Polls API",
        default_version='v1',
        description="API docs for Online Polls (Project Nexus)",
        terms_of_service="https://www.swaggerui.com/terms/",
        contact=openapi.Contact(email="vincentcollins690@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', landing, name='landing'),
    path('admin/', admin.site.urls),
    # Auth (JWT)
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # App routes
    path('api/', include('polls.urls')),   # e.g. /api/polls/

    # API docs
    re_path(r'^api/docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)