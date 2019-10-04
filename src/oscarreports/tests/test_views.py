from datetime import timedelta
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from psycopg2.extras import DateTimeTZRange
from oscar.test.testcases import WebTestCase
from webtest.app import AppError
from .. import models


class ReportsDashboardTests(WebTestCase):
    is_staff = True

    def test_dashboard_is_accessible_to_staff(self):
        url = reverse('dashboard:reports-index')
        response = self.get(url)
        self.assertIsOk(response)


    def test_conditional_offers_no_date_range(self):
        url = reverse('dashboard:reports-index')
        response = self.get(url)

        response.form['report_type'] = 'conditional-offers'
        response.form.submit()
        self.assertIsOk(response)


    def test_conditional_offers_with_date_range(self):
        url = reverse('dashboard:reports-index')
        response = self.get(url)

        response.form['report_type'] = 'conditional-offers'
        response.form['date_from'] = '2017-01-01'
        response.form['date_to'] = '2017-12-31'
        response.form.submit()
        self.assertIsOk(response)


    def test_conditional_offers_with_invalid_date_range(self):
        url = reverse('dashboard:reports-index')
        response = self.get(url)

        response.form['report_type'] = 'conditional-offers'
        response.form['date_from'] = '2017-12-31'
        response.form['date_to'] = '2017-01-01'
        response.form.submit()
        self.assertIsOk(response)



class DownloadReportDashboardTests(WebTestCase):
    is_staff = True

    def setUp(self):
        super().setUp()
        self.staff_user = User.objects.create_user(
            username='root',
            email='root@example.com',
            is_staff=True)
        self.report = models.Report()
        self.report.uuid = 'd3c74a8b-e7ae-4482-bd9c-bee69fde5c5c'
        self.report.content_type = None
        self.report.owner = self.staff_user
        self.report.type_code = 'order_report'
        self.report.date_range = DateTimeTZRange(
            lower=(timezone.now() - timedelta(days=1)),
            upper=(timezone.now()))
        self.report.save()


    def test_download_not_found(self):
        url = reverse('dashboard:reports-download', args=[self.report.uuid])
        with self.assertRaises(AppError):
            self.get(url)


    def test_download_report(self):
        self.report.generate()
        url = reverse('dashboard:reports-download', args=[self.report.uuid])
        response = self.get(url)
        self.assertIsOk(response)



class DeleteReportDashboardTests(WebTestCase):
    is_staff = True

    def setUp(self):
        super().setUp()
        self.staff_user = User.objects.create_user(
            username='root',
            email='root@example.com',
            is_staff=True)
        self.report = models.Report()
        self.report.uuid = 'd3c74a8b-e7ae-4482-bd9c-bee69fde5c5c'
        self.report.content_type = None
        self.report.owner = self.staff_user
        self.report.type_code = 'order_report'
        self.report.date_range = DateTimeTZRange(
            lower=(timezone.now() - timedelta(days=1)),
            upper=(timezone.now()))
        self.report.save()


    def test_dashboard_is_accessible_to_staff(self):
        url = reverse('dashboard:reports-delete', args=[self.report.uuid])
        response = self.get(url)
        self.assertIsOk(response)


    def test_can_delete_report(self):
        self.assertEqual(models.Report.objects.count(), 1)
        url = reverse('dashboard:reports-delete', args=[self.report.uuid])
        response = self.get(url)
        response.form.submit()
        self.assertIsOk(response)
        self.assertEqual(models.Report.objects.count(), 0)
