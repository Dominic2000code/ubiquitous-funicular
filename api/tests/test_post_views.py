from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from posts.models import TextPost, VideoPost, ImagePost
from django.core.files.storage import default_storage
import io

User = get_user_model()


class PostViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.text_post = TextPost.objects.create(
            author=self.user, content='This is a test content.')

        self.image_data = open('media/no_image.png', 'rb').read()
        self.image_post = ImagePost.objects.create(
            author=self.user, image=SimpleUploadedFile(
                'test_image.jpg', self.image_data, content_type='image/png')
        )

        self.video_data = open('media/test_video.mp4', 'rb').read()
        self.video_post = VideoPost.objects.create(
            author=self.user, video=File(
                io.BytesIO(self.video_data), name='test_video.mp4'
            )
        )

    def delete_files(self, file_paths):
        for file_path in file_paths:
            if file_path:
                default_storage.delete(file_path)

    def tearDown(self):
        uploaded_images = ImagePost.objects.values_list('image', flat=True)
        uploaded_videos = VideoPost.objects.values_list('video', flat=True)

        self.delete_files(uploaded_images)
        self.delete_files(uploaded_videos)

        default_storage.delete('post_images/test_image.jpg')
        default_storage.delete('post_videos/test_video.mp4')
        default_storage.delete('post_videos/video')

    def test_create_text_post(self):
        url = reverse('api:textpost-list-create')
        data = {'author': self.user.id, 'content': 'This is a test content.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TextPost.objects.count(), 2)

    def test_get_text_post(self):
        url = reverse('api:textpost-detail', args=[self.text_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], 'This is a test content.')

    def test_update_text_post(self):
        url = reverse('api:textpost-detail', args=[self.text_post.id])
        data = {'content': 'Updated test content.'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], 'Updated test content.')

    def test_delete_text_post(self):
        url = reverse('api:textpost-detail', args=[self.text_post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(TextPost.objects.count(), 0)

    def test_create_image_post(self):
        url = reverse('api:imagepost-list-create')
        data = {'author': self.user.id, 'image': SimpleUploadedFile(
            'test_image.jpg', self.image_data, content_type='image/jpeg')}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ImagePost.objects.count(), 2)

    def test_get_image_post(self):
        url = reverse('api:imagepost-detail', args=[self.image_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_image_post(self):
        url = reverse('api:imagepost-detail', args=[self.image_post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(ImagePost.objects.count(), 0)

    def test_create_video_post(self):
        url = reverse('api:videopost-list-create')
        data = {'author': self.user.id, 'video': File(
            io.BytesIO(self.video_data))}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VideoPost.objects.count(), 2)

    def test_get_video_post(self):
        url = reverse('api:videopost-detail', args=[self.video_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_video_post(self):
        url = reverse('api:videopost-detail', args=[self.video_post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(VideoPost.objects.count(), 0)
