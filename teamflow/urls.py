from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name="schema"), 
    path('api/docs/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    
    path('api/', include('workspaces.urls')),
    path('api/', include('projects.urls')),
    path('api/', include('accounts.urls')),
    
    path('api-auth/', include('rest_framework.urls')),
]
