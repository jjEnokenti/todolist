from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    include,
    path
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('goals/', include('goals.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
