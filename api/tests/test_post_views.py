from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from posts.models import TextPost, VideoPost, ImagePost, Repost, Comment, Reply, Post
from django.core.files.storage import default_storage
from django.conf import settings
import io
import redis

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

        self.repost = Repost.objects.create(
            original_post=self.text_post, user=self.user)

        self.comment_data = {
            'author': self.user,
            'content': 'This is a comment.'
        }
        self.comment = Comment.objects.create(**self.comment_data)

        self.reply_data = {
            'author': self.user,
            'content': 'This is a reply.',
            'parent_comment': self.comment
        }
        self.reply = Reply.objects.create(**self.reply_data)

        self.r = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=settings.TEST_REDIS_DB)

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
        self.r.delete(f'post:likes_count:{self.text_post.id}')

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

    # def test_toggle_like_view(self):
    #     url = reverse('api:toggle-like', args=[self.text_post.id])
    #     response = self.client.post(url)
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data['likes_count'], 1)

    #     # Test toggling the like
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data['likes_count'], 0)

    def test_create_repost(self):
        url = reverse('api:repost', args=[self.image_post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Repost.objects.count(), 2)

    def test_get_repost_list(self):
        url = reverse('api:repost-list', args=[self.text_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['user'], self.user.id)

    def test_get_repost_list_nonexistent_post(self):
        url = reverse('api:repost-list', args=[999])  # Nonexistent post ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_create_comment_view(self):
        url = reverse('api:post-comment-list', args=[self.text_post.id])
        data = {
            'author': self.user.id,
            'content': 'This is a comment content.'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'],
                         data['content'])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_update_destroy_comment_view(self):
        self.text_post.comments.add(self.comment)
        url = reverse('api:post-comment-detail',
                      args=[self.text_post.id, self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'],
                         self.comment_data['content'])

        updated_content = 'Updated comment content.'
        response = self.client.patch(url, data={
            'content': updated_content})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], updated_content)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_list_create_reply_view(self):
        url = reverse('api:comment-reply-list',
                      args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        data = {
            'author': self.user.id,
            'content': 'This is a reply.',
            'parent_comment': self.comment.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], self.reply_data['content'])

    def test_retrieve_update_destroy_reply_view(self):
        url = reverse('api:comment-reply-detail',
                      args=[self.comment.id, self.reply.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], self.reply_data['content'])

        updated_content = 'Updated reply content.'
        response = self.client.patch(url, data={
            'content': updated_content})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], updated_content)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
