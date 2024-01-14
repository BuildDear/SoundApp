from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from src.audio_lib.models import Genre, License
from src.oauth.models import AuthUser


class GenreViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_genre_list(self):
        Genre.objects.create(name='Rock')
        Genre.objects.create(name='Pop')

        response = self.client.get('/genre/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


