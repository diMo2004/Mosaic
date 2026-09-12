from django.test import TestCase
from unittest.mock import patch
# Create your tests here.
#User can register
#User can login
#Login returns access + refresh
#Invalid login fails
#Protected endpoint rejects unauthenticated request

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import UserProfile

class GoogleAuthTests(APITestCase):
    @patch('users.views.google_id_token.verify_oauth2_token')
    def test_google_login_new_user_requires_profile_completion(self, mock_verify):
        mock_verify.return_value = {
            'email': 'newstudent@example.com',
            'name': 'New Student',
            'given_name': 'New',
            'family_name': 'Student',
            'picture': 'https://example.com/avatar.jpg',
        }

        response = self.client.post(
            '/api/auth/google-auth/',
            {
                'id_token': 'valid-mock-token',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "profile_required")
        self.assertIn('education_level', response.data['missing_fields'])
        self.assertIn('learning_goal', response.data['missing_fields'])
        self.assertTrue(User.objects.filter(email="newstudent@example.com").exists())

    @patch('users.views.google_id_token.verify_oauth2_token')
    def test_google_login_existing_completed_user_authenticates(self, mock_verify):
        user = User.objects.create_user(username="existing", email="existing@example.com")
        user.profile.full_name = "Existing Student"
        user.profile.education_level = "Undergraduate"
        user.profile.learning_goal = "Master Algorithms"
        user.profile.profile_completed = True
        user.profile.save()

        mock_verify.return_value = {
            'email': 'existing@example.com',
            'name': 'Existing Student',
        }

        response = self.client.post(
            '/api/auth/google-auth/',
            {'id_token': 'valid-mock-token'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "authenticated")
        self.assertIn('access', response.data)

    @patch('users.views.google_id_token.verify_oauth2_token')
    def test_invalid_google_token_returns_400(self, mock_verify):
        mock_verify.side_effect = ValueError("Token expired")
        response = self.client.post(
            '/api/auth/google-auth/',
            {'id_token': 'invalid-token'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid Google token.")

    def test_complete_profile_flow(self):
        user = User.objects.create_user(username="incomplete", email="inc@example.com")
        self.client.force_authenticate(user=user)

        res_fail = self.client.post(
            '/api/auth/complete-profile/',
            {'full_name': 'Incomplete User', 'education_level': 'Undergrad'},
            format='json',
        )
        self.assertEqual(res_fail.status_code, status.HTTP_400_BAD_REQUEST)

        res_success  =self.client.post(
            '/api/auth/complete-profile/',
            {
                'full_name': 'Completed User',
                'education_level': 'Undergraduate',
                'learning_goal': 'Prepare for Gate CSE',
                'interests': ['Algorithms', 'Operating Systems'],
            },
            format='json',
        )
        self.assertEqual(res_success.status_code, status.HTTP_200_OK)
        self.assertTrue(res_success.data['profile_completed'])
        user.profile.refresh_from_db()
        self.assertTrue(user.profile.profile_completed)


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