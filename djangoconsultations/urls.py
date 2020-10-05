from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('consultations/', include('consultations.urls')),  # allows referencing other urls.py file
    path('accounts/', include('accounts.urls'))             # allows referencing other urls.py file
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
