from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path ,  include
from media.views import UploadView, ViewView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/', include('media.urls')),  # Adjust to match your app
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
