from django.test import TestCase

# Create your tests here.
#User can register
#User can login
#Login returns access + refresh
#Invalid login fails
#Protected endpoint rejects unauthenticated request

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class AuthTests(APITestCase):
    def test_user_can_register(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpassword123',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_can_login_and_receive_tokens(self):
        User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123',
        )

        response = self.client.post(
            '/api/auth/login/',
            {
                'username': 'testuser',
                'password': 'testpassword123',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login_fails(self):
        response = self.client.post(
            '/api/auth/login/',
            {
                'username': 'missing',
                'password': 'wrongpassword',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)