from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.parsers import MultiPartParser
from rest_framework.test import force_authenticate, APIClient

from ..models import Genre, License, Album, Track
from ..serializer import GenreSerializer, LicenseSerializer, AlbumSerializer, CreateAuthorTrackSerializer
from ...oauth.models import AuthUser


class GenreSerializerTest(TestCase):

    def setUp(self):
        self.genre_data = {'ID': 1, 'name': 'Rock'}
        self.genre = Genre.objects.create(name='Pop')

    def test_serialization(self):
        serializer = GenreSerializer(instance=self.genre)
        serialized_data = serializer.data
        print(serializer.data)
        self.assertEqual(serialized_data['name'], self.genre.name)

    def test_deserialization(self):
        serializer = GenreSerializer(data=self.genre_data)
        self.assertTrue(serializer.is_valid())
        deserialized_data = serializer.validated_data
        self.assertEqual(deserialized_data['name'], self.genre_data['name'])


class LicenseSerializerTest(TestCase):

    def setUp(self):
        self.user = AuthUser.objects.create(email='test@example.com', password='testpass')
        self.license_data = {'id': 1, 'text': 'Test License Text', 'user': self.user.id}
        self.license = License.objects.create(user=self.user, text='Test License Text')

    def test_serialization(self):
        serializer = LicenseSerializer(instance=self.license)
        serialized_data = serializer.data
        self.assertEqual(serialized_data['id'], self.license.id)
        self.assertEqual(serialized_data['text'], self.license.text)

    def test_deserialization(self):
        serializer = LicenseSerializer(data=self.license_data)
        self.assertTrue(serializer.is_valid())
        deserialized_data = serializer.validated_data
        self.assertEqual(deserialized_data['text'], self.license_data['text'])


class AlbumSerializerTest(TestCase):

    def setUp(self):
        self.user = AuthUser.objects.create(email='test@example.com', password='testpass')
        self.album_data = {
            'id': 1,
            'name': 'Test Album',
            'description': 'Test Album Description',
            'private': False,
            'cover': None,  # Replace with the actual file or use a mock file
        }
        self.album = Album.objects.create(user=self.user, **self.album_data)

    def test_serialization(self):
        serializer = AlbumSerializer(instance=self.album)
        expected_data = {
            'id': self.album.id,
            'name': 'Test Album',
            'description': 'Test Album Description',
            'private': False,
            'cover': None,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialization(self):
        serializer = AlbumSerializer(data=self.album_data)
        self.assertTrue(serializer.is_valid())
        deserialized_data = serializer.validated_data
        self.assertEqual(deserialized_data['name'], 'Test Album')
        self.assertEqual(deserialized_data['description'], 'Test Album Description')
        self.assertEqual(deserialized_data['private'], False)


class CreateAuthorTrackSerializerTest(TestCase):
    def setUp(self):
        self.user = AuthUser.objects.create(email='test@example.com', password='testpass')
        self.client = APIClient()
        self.parser = MultiPartParser()

    def test_create_track(self):
        force_authenticate(request=self.client, user=self.user)

        license_data = {'id': 1, 'text': 'Test License', 'user': self.user.id}
        license_response = self.client.post('/license/', license_data, format='json')
        self.assertEqual(license_response.status_code, 201)
        license_id = license_response.data['id']

        # Expected data for creating a track
        data = {
            'title': 'Test Track',
            'license': license_id,
            'genre': [Genre.objects.create(name='Test Genre').id],
            'album': Album.objects.create(name='Test Album', user=self.user).id,
            'link_of_author': 'http://example.com/author',
            'file': SimpleUploadedFile("test_track.mp3", b"file_content", content_type="audio/mp3"),
            'private': False,
            'cover': SimpleUploadedFile("test_cover.jpg", b"file_content", content_type="image/jpeg"),
        }

        # Make a POST request to create a track
        response = self.client.post('/track/', data, format='multipart')

        # Check if the response status code is 201 (created)
        self.assertEqual(response.status_code, 201)

        # Get the created track from the database
        created_track = Track.objects.get(title='Test Track')

        # Check if the serialized data of the created track matches the expected data
        serializer = CreateAuthorTrackSerializer(created_track)
        self.assertEqual(response.data, serializer.data)

        # Check if files were deleted
        self.assertFalse(created_track.file.storage.exists(created_track.file.name))
        self.assertFalse(created_track.cover.storage.exists(created_track.cover.name))