from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("careerbot.urls")),
    path("__reload__/",include("django_browser_reload.urls")),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
