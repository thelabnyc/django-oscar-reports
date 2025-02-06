from django.conf import settings


def overridable(name: str, default: str = "") -> str:
    return getattr(settings, name, default)


# Directory prefix used when uploading generated reports to storage
OSCAR_REPORTS_UPLOAD_PREFIX: str = overridable(
    "OSCAR_REPORTS_UPLOAD_PREFIX", "oscar-reports"
)
