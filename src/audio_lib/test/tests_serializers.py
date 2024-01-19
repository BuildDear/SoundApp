from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.test import force_authenticate, APIClient

from ..models import Genre, License, Album, Track, PlayList
from ..serializer import (
    GenreSerializer,
    LicenseSerializer,
    AlbumSerializer,
    CreateAuthorTrackSerializer,
    CreatePlayListSerializer,
    PlayListSerializer,
)
from ...oauth.models import AuthUser


class GenreSerializerTest(TestCase):
    def setUp(self):
        self.genre_data = {"ID": 1, "name": "Rock"}
        self.genre = Genre.objects.create(name="Pop")

    def test_serialization(self):
        serializer = GenreSerializer(instance=self.genre)
        serialized_data = serializer.data
        print(serializer.data)
        self.assertEqual(serialized_data["name"], self.genre.name)

    def test_deserialization(self):
        serializer = GenreSerializer(data=self.genre_data)
        self.assertTrue(serializer.is_valid())
        deserialized_data = serializer.validated_data
        self.assertEqual(deserialized_data["name"], self.genre_data["name"])


class LicenseSerializerTest(TestCase):
    def setUp(self):
        self.user = AuthUser.objects.create(
            email="test@example.com", password="testpass"
        )
        self.license_data = {"id": 1, "text": "Test License Text", "user": self.user.id}
        self.license = License.objects.create(user=self.user, text="Test License Text")

    def test_serialization(self):
        serializer = LicenseSerializer(instance=self.license)
        serialized_data = serializer.data
        self.assertEqual(serialized_data["id"], self.license.id)
        self.assertEqual(serialized_data["text"], self.license.text)

    def test_deserialization(self):
        serializer = LicenseSerializer(data=self.license_data)
        self.assertTrue(serializer.is_valid())
        deserialized_data = serializer.validated_data
        self.assertEqual(deserialized_data["text"], self.license_data["text"])


class AlbumSerializerTest(TestCase):
    def setUp(self):
        self.user = AuthUser.objects.create(
            email="test@example.com", password="testpass"
        )
        self.album_data = {
            "id": 1,
            "name": "Test Album",
            "description": "Test Album Description",
            "private": False,
            "cover": None,
        }
        self.album = Album.objects.create(user=self.user, **self.album_data)

    def test_serialization(self):
        serializer = AlbumSerializer(instance=self.album)
        expected_data = {
            "id": self.album.id,
            "name": "Test Album",
            "description": "Test Album Description",
            "private": False,
            "cover": None,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialization(self):
        serializer = AlbumSerializer(data=self.album_data)
        self.assertTrue(serializer.is_valid())
        deserialized_data = serializer.validated_data
        self.assertEqual(deserialized_data["name"], "Test Album")
        self.assertEqual(deserialized_data["description"], "Test Album Description")
        self.assertEqual(deserialized_data["private"], False)


class CreateAuthorTrackSerializerTest(TestCase):
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

    def test_create_track_serialization(self):
        user = AuthUser.objects.get(email="matema.group1@gmail.com")
        license = License.objects.create(text="some text", user=user)
        genre = Genre.objects.create(name="genre")

        track = Track.objects.create(title="track", license=license, user=user)
        track.genre.add(genre)

        serializer = CreateAuthorTrackSerializer(instance=track)
        print(serializer.data)


class CreatePlayListSerializerTest(TestCase):
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
        print(self.user)

        response = self.client.post("/auth/jwt/create/", login_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, "Failed to obtain JWT token"
        )

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        self.playlist_data = {
            "title": "Test Playlist",
            "cover": None,
        }
        self.album = PlayList.objects.create(user=self.user, **self.playlist_data)

    def test_create_playlist_serialization(self):
        playlist = PlayList.objects.get(title="Test Playlist")
        serializer = PlayListSerializer(instance=playlist)
        expected_data = {
            "id": 2,
            "title": "Test Playlist",
            "tracks": [],
            "cover": None,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_create_playlist_deserialization(self):
        serializer = CreatePlayListSerializer(data=self.playlist_data)
        self.assertTrue(serializer.is_valid())
        deserialized_data = serializer.validated_data
        self.assertEqual(deserialized_data["title"], "Test Playlist")
