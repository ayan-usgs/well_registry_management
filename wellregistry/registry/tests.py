"""
Tests for the registry application

"""

from django.test import RequestFactory, TestCase

from .views import BasePage


class TestBasePage(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_base_page(self):
        req = self.factory.get('/registry')
        resp = BasePage.as_view()(req)
        self.assertEqual(resp.status_code, 200)