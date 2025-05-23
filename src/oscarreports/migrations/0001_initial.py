# Generated by Django 2.2.6 on 2019-10-03 21:12

import uuid

from django.conf import settings
from django.db import migrations, models
import django.contrib.postgres.fields.ranges
import django.db.models.deletion
import oscar.models.fields

import oscarreports.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "type_code",
                    models.CharField(max_length=50, verbose_name="Type Code"),
                ),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "date_range",
                    django.contrib.postgres.fields.ranges.DateTimeRangeField(
                        blank=True, null=True, verbose_name="Date Range"
                    ),
                ),
                (
                    "task_id",
                    models.UUIDField(
                        blank=True,
                        editable=False,
                        null=True,
                        unique=True,
                        verbose_name="Background Task ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created On"),
                ),
                (
                    "queued_on",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Queued On"
                    ),
                ),
                (
                    "started_on",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Started On"
                    ),
                ),
                (
                    "completed_on",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Completed On"
                    ),
                ),
                (
                    "mime_type",
                    oscar.models.fields.NullCharField(
                        max_length=20, verbose_name="MIME Type"
                    ),
                ),
                (
                    "report_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=oscarreports.models.get_report_upload_path,
                        verbose_name="Report File",
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="contenttypes.ContentType",
                        verbose_name="Content Type",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner",
                    ),
                ),
            ],
        ),
    ]
