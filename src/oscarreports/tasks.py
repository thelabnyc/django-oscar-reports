from __future__ import absolute_import, annotations

from uuid import UUID

from celery import shared_task


@shared_task(ignore_result=True)
def generate_report(report_uuid: str | UUID, report_format: str) -> None:
    from . import models

    report = models.Report.objects.get(uuid=report_uuid)
    report.generate(report_format)
