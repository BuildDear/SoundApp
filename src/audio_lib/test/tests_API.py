from rest_framework.test import APITestCase
from rest_framework import status
from src.audio_lib.models import Genre


class GenreListAPITests(APITestCase):
    def setUp(self):
        self.genre_data = {"name": "Rock"}
        self.genre = Genre.objects.create(name="Pop")

    def test_get_genres(self):
        response = self.client.get('/genre/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_genres_invalid_path(self):
        response = self.client.get('/wrong_path/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_genres_wrong_method(self):
        response = self.client.post('/genre/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
