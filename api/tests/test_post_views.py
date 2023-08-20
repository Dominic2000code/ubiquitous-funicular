from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import TextPost, VideoPost, ImagePost
from django.core.files.storage import default_storage

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

    def tearDown(self):
        uploaded_images = ImagePost.objects.values_list('image', flat=True)
        for image_path in uploaded_images:
            if image_path:
                print('deleted:', image_path)
                default_storage.delete(image_path)
        default_storage.delete('post_images/test_image.jpg')

    def test_create_text_post(self):
        url = reverse('api:textpost-list-create')
        data = {'author': self.user.id, 'content': 'This is a test content.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TextPost.objects.count(), 2)

    def test_get_text_post(self):
        url = reverse('api:textpost-detail', args=[self.user.id])
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
        # Adjust the URL name and argument
        url = reverse('api:imagepost-detail', args=[self.image_post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(ImagePost.objects.count(), 0)
