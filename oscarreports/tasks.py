from __future__ import annotations

from uuid import UUID

from django_tasks import task


@task()
def generate_report(report_uuid: str, report_format: str) -> None:
    from . import models

    report = models.Report.objects.get(uuid=UUID(report_uuid))
    report.generate(report_format)
