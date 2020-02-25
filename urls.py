from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# admin.site.site_header = 'Example'
# admin.site.site_title = 'Example'

if settings.DEBUG:
    docs_permissions = ()
else:
    docs_permissions = (permissions.IsAuthenticated,)

schema_view = get_schema_view(
   openapi.Info(
      title="OPEN API",
      default_version='v1'
   ),
   public=False,
   permission_classes=docs_permissions,
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
