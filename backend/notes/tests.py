from django.test import TestCase

# Create your tests here.
#Authenticated user can upload note
#Unauthenticated user cannot upload note
#Profile-complete users can list their own notes
#Users cannot list or view another user's note

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from notes.models import Note

class NotePermissionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )
        self.user.profile.profile_completed = True
        self.user.profile.save()

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpassword123',
        )

        self.other_user.profile.profile_completed = True
        self.other_user.profile.save()

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

    def test_upload_falls_back_to_inline_processing_when_broker_is_unavailable(self):
        self.client.force_authenticate(user=self.user)
        file = SimpleUploadedFile('note.txt', b'BFS uses a queue', content_type='text/plain')

        with patch('notes.views.process_note_task.delay', side_effect=ConnectionError('broker unavailable')):
            with patch('notes.views.NoteProcessingService.process') as process_inline:
                with self.captureOnCommitCallbacks(execute=True):
                    response = self.client.post(
                        '/api/notes/upload/',
                        {'title': 'Algorithms Note', 'file': file},
                        format='multipart',
                    )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        process_inline.assert_called_once_with(response.data['id'])

    def test_user_can_list_only_own_notes(self):
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

    def test_user_can_retrieve_own_note_but_not_another_users_note(self):
        own_note = Note.objects.create(owner=self.user, title='Mine', file='notes/mine.txt')
        other_note = Note.objects.create(owner=self.other_user, title='Not Mine', file='notes/not_mine.txt')
        self.client.force_authenticate(user=self.user)

        own_response = self.client.get(f'/api/notes/{own_note.id}/')
        other_response = self.client.get(f'/api/notes/{other_note.id}/')

        self.assertEqual(own_response.status_code, status.HTTP_200_OK)
        self.assertEqual(other_response.status_code, status.HTTP_404_NOT_FOUND)

    
