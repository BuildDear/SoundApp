from rest_framework.parsers import MultiPartParser
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from src.audio_lib.models import Genre, License
from src.audio_lib.serializer import LicenseSerializer
from src.oauth.models import AuthUser


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


class LicenseViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.parser = MultiPartParser()
        super().setUp()
        self.create_active_user_and_get_token()

    def create_active_user_and_get_token(self):
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

        # Створення тестової ліцензії для цього користувача
        self.license_data = {"text": "Test license text"}
        self.license = License.objects.create(user=self.user, **self.license_data)

    def test_create_license(self):
        url = '/license/'
        response = self.client.post(url, self.license_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_license(self):
        url = f'/license/{self.license.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, LicenseSerializer(self.license).data)

    def test_update_license(self):
        url = f'/license/{self.license.id}/'
        updated_data = {"text": "Updated license text"}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.license.refresh_from_db()
        self.assertEqual(self.license.text, updated_data["text"])

    def test_delete_license(self):
        url = f'/license/{self.license.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(License.objects.filter(id=self.license.id).exists())