from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = __package__

sub_dir = f'{settings.SUB_DIR}/' if settings.SUB_DIR else ''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('superman/api/', include('api.urls')),
    path('', views.home)
]

# cabsulate everything in a subdirectery
urlpatterns = [
    path(sub_dir, include(urlpatterns))
]

# appending static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
