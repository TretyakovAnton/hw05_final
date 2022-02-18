from django.test import TestCase
from django.test.client import RequestFactory

from ..views import page_not_found, server_error, permission_denied


class TestErrorPages(TestCase):
    """Проверяем кастомные шаблоны."""
    def test_error_handlers(self):
        factory = RequestFactory()
        request = factory.get('/')
        response = page_not_found(request, Exception('Page not Found'))
        self.assertEqual(response.status_code, 404)
        response = server_error(request)
        self.assertEqual(response.status_code, 500)
        response = permission_denied(request, Exception('Permission Denied'))
        self.assertEqual(response.status_code, 403)
