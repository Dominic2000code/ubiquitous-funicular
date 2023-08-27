from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from notifications.notification import create_comment_notification, create_follow_notification
from posts.models import TextPost

User = get_user_model()


class NotificationViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')
        self.user2 = User.objects.create_user(
            username='user2', password='password')
        self.post = TextPost.objects.create(
            author=self.user1, content="Text post")
        self.notification1 = create_follow_notification(self.user2, self.user1)
        self.notification2 = create_comment_notification(
            self.user2, self.post)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_notification_list_view(self):
        url = reverse('api:user-notifications',
                      kwargs={'user_id': self.user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_notification_mark_read_view(self):
        url = reverse('api:mark-notification-read',
                      kwargs={'pk': self.notification1.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 200)
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
