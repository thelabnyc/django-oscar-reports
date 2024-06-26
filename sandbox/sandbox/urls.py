from django.apps import apps
from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf.urls import i18n as i18n_urls
from django.views.static import serve


urlpatterns = [
    path("i18n/", include(i18n_urls)),
    path("admin/", admin.site.urls),
    path(
        "media/<path:path>",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
    ),
    # Include Oscar
    path("", include(apps.get_app_config("oscar").urls[0])),
]
