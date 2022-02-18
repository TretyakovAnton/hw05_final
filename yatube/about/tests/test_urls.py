from django.test import TestCase, Client

from http import HTTPStatus


class StaticURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_author(self):
        response = self.client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech(self):
        response = self.client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
