from io import BytesIO
from unittest import TestCase

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from src.audio_lib.models import Genre, License, Album
from src.audio_lib.serializer import LicenseSerializer
from src.oauth.models import AuthUser


class BaseTestCase(APITestCase):

    def create_dummy_image(self):
        file = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')  # Create a red image
        image.save(file, 'JPEG')
        file.seek(0)
        return ContentFile(file.read(), 'test.jpg')

    def setUp(self):
        self.client = APIClient()
        self.parser = MultiPartParser()

        active_user_data = {
            "email": "matema.group1@gmail.com",
            "password": "OLGGG1234olggg!!!***1234",
            "re_password": "OLGGG1234olggg!!!***1234",
        }
        login_data = {
            "email": "matema.group1@gmail.com",
            "password": "OLGGG1234olggg!!!***1234",
        }

        response = self.client.post("/auth/users/", active_user_data, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Failed to create active user",
        )

        self.user = AuthUser.objects.get(email="matema.group1@gmail.com")

        response = self.client.post("/auth/jwt/create/", login_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, "Failed to obtain JWT token"
        )

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        self.license_data = {"text": "Test license text"}
        self.license = License.objects.create(user=self.user, **self.license_data)

        self.album_data = {
            'name': 'Test Album',
            'description': 'Test Album Description',
            'private': False,
            'cover': self.create_dummy_image(),
        }
        self.album = Album.objects.create(user=self.user, **self.album_data)


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


class LicenseAPITests(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_create_license(self):
        url = '/license/'
        response = self.client.post(url, self.license_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_license(self):
        url = f'/license/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data[0]
        self.assertEqual(response_data, LicenseSerializer(self.license).data)

    def test_update_license(self):
        url = f'/license/{self.license.id}'
        updated_data = {"text": "Updated license text"}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.license.refresh_from_db()
        self.assertEqual(self.license.text, updated_data["text"])

    def test_delete_license(self):
        url = f'/license/{self.license.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(License.objects.filter(id=self.license.id).exists())


class AlbumAPITest(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_create_album(self):
        url = '/album/'
        album_data = {
            'name': 'New Test Album',
            'description': 'New Test Album Description',
            'private': False,
            'cover': self.create_dummy_image(),
        }
        response = self.client.post(url, album_data, format='multipart')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_albums(self):
        response = self.client.get('/album/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_album(self):
        data = {
            'name': 'New Album',
            'description': 'New Album Description',
            'private': True,

        }
        response = self.client.put(f'/album/{self.album.id}/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_album(self):
        response = self.client.delete(f'/album/{self.album.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Album.objects.filter(pk=self.album.pk).exists())
