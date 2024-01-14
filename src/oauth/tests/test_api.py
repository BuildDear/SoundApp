
from django.test import TestCase, Client
from django.urls import reverse


class GoogleTest(TestCase):
    def test_google_login_view(self):
        client = Client()
        response = client.get(reverse('google-login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'google_login.html')

