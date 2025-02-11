# resume_builder/urls.py (or your project’s main urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('resumes/', include('resumes.urls')),  # Assuming 'resume' is your main app for resume features
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
