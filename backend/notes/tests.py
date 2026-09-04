from django.test import TestCase

# Create your tests here.
#Authenticated user can upload note
#Unauthenticated user cannot upload note
#Normal user cannot list notes
#Premium/contributor user can list own notes
#Premium/contributor user cannot view another user's note

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from notes.models import Note

class NotePermissionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpassword123',
        )

    def test_authenticated_user_can_upload_note(self):
        self.client.force_authenticate(user=self.user)
        file = SimpleUploadedFile(
            'note.txt',
            b'BFS uses a queue',
            content_type='text/plain',
        )
        response = self.client.post(
            '/api/notes/upload/',
            {
                'title': 'Algorithms Note',
                'file': file,
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.first().owner, self.user)

    def test_normal_user_cannot_list_notes(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_permission_can_list_own_notes(self):
        self.user.profile.can_view_own_notes = True  # Simulating a user with permission
        self.user.profile.save()
        Note.objects.create(
            owner=self.user,
            title='Mine',
            file='notes/mine.txt',
        )
        Note.objects.create(
            owner=self.other_user,
            title='Not Mine',
            file='notes/not_mine.txt',
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Mine')

    