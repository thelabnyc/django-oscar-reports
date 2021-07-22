from django.apps import apps
from django.conf import settings
from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin
from django.conf.urls import i18n as i18n_urls
from django.views.static import serve


urlpatterns = [
    re_path(r"^i18n/", include(i18n_urls)),
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
    ),
    # Include Oscar
    re_path(r"^", include(apps.get_app_config("oscar").urls[0])),
]
