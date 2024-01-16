from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.utils import json

from src.oauth.models import SocialLink, AuthUser
from src.oauth.serializer import SocialLinkSerializer, GoogleAuth, AuthorSerializer


class AuthUserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'example@gmail.com',
            'password': '12345678',
        }
        self.user = AuthUser.objects.create_user(**self.user_data)

    def test_registration_serializer_valid_data(self):
        client = APIClient()

        request_data = {
            "user": {
                "email": "letschuka@gmail.com",
                "password": "12345678"
            }
        }
        response = client.post('/users/', json.dumps(request_data), content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_registration_serializer_invalid_data(self):
        client = APIClient()
        invalid_user_data = {
            'email': 'invalidemail',
            'password': 'short',
        }
        response = client.post('/users/', invalid_user_data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', response.data)

    def test_user_serializer_authenticated_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.get('/me/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('avatar', response.data)
        self.assertIn('country', response.data)

    def test_user_serializer_unauthenticated_user(self):
        client = APIClient()
        response = client.get('/me/')

        self.assertEqual(response.status_code, 403)

    def test_social_link_serializer(self):
        social_link_data = {
            'link': 'http://example.com',
            'user': self.user
        }
        social_link = SocialLink.objects.create(**social_link_data)

        serializer = SocialLinkSerializer(social_link)
        serialized_data = serializer.data

        self.assertEqual(serialized_data['link'], social_link_data['link'])

    def test_author_serializer(self):
        user = AuthUser.objects.create_user(email='example11@gmail.com', password='12345678')

        author_data = {
            'id': 5,
            'avatar': 'http://example.com/avatar.jpg',
            'country': 'Test Country',
            'city': 'Test City',
            'bio': 'Test Bio',
            'display_name': 'Test User',
            'social_links': [{'id': 1, 'link': 'http://social1.com'}, {'id': 2, 'link': 'https://social2.com'}],
        }

        serializer = AuthorSerializer(instance=user, data=author_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data

        self.assertEqual(serialized_data['id'], author_data['id'])
        self.assertEqual(serialized_data['avatar'], author_data['avatar'])
        self.assertEqual(serialized_data['country'], author_data['country'])
        self.assertEqual(serialized_data['city'], author_data['city'])
        self.assertEqual(serialized_data['bio'], author_data['bio'])
        self.assertEqual(serialized_data['display_name'], author_data['display_name'])

        self.assertEqual(len(serialized_data['social_links']), len(author_data['social_links']))
        for i in range(len(author_data['social_links'])):
            self.assertEqual(serialized_data['social_links'][i]['link'], author_data['social_links'][i]['link'])

    def test_google_auth_serializer_valid_data(self):
        valid_google_auth_data = {
            'email': 'test@gmail.com',
            'token': 'testtoken',
        }

        serializer = GoogleAuth(data=valid_google_auth_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.validated_data

        self.assertEqual(serialized_data['email'], valid_google_auth_data['email'])
        self.assertEqual(serialized_data['token'], valid_google_auth_data['token'])

    def test_google_auth_serializer_invalid_data(self):
        invalid_google_auth_data = {
            'email': 'invalidemail',
            'token': '',
        }

        serializer = GoogleAuth(data=invalid_google_auth_data)
        self.assertFalse(serializer.is_valid())

        self.assertIn('email', serializer.errors)
        self.assertIn('token', serializer.errors)
