from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import TextPost
from groups.models import Group
from .notification import (
    create_comment_notification,
    create_follow_notification,
    create_join_group_notification,
    create_leave_group_notification,
    create_unfollow_notification
)

User = get_user_model()


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')
        self.user2 = User.objects.create_user(
            username='user2', password='password')
        self.post = TextPost.objects.create(
            author=self.user1, content='Test content')
        self.group = Group.objects.create(
            name='Test Group', creator=self.user1)

    def test_create_comment_notification(self):
        notification = create_comment_notification(
            sender=self.user2, post=self.post)
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.notification_type, 'comment')
        self.assertEqual(notification.post, self.post)
        self.assertEqual(notification.message,
                         'user2 has commented on your post.')

    def test_create_join_group_notification(self):
        notification = create_join_group_notification(
            user=self.user2, group=self.group)
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.notification_type, 'join_group')
        self.assertEqual(notification.group, self.group)
        self.assertEqual(notification.message,
                         "user2 has joined the group 'Test Group'.")

    def test_create_leave_group_notification(self):
        notification = create_leave_group_notification(
            user=self.user2, group=self.group)
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.notification_type, 'leave_group')
        self.assertEqual(notification.group, self.group)
        self.assertEqual(notification.message,
                         "user2 has left the group 'Test Group'.")

    def test_create_follow_notification(self):
        notification = create_follow_notification(
            follower=self.user2, recipient=self.user1)
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.notification_type, 'follow')
        self.assertEqual(notification.follower, self.user2)
        self.assertEqual(notification.message,
                         'user2 has started following you.')

    def test_create_unfollow_notification(self):
        notification = create_unfollow_notification(
            follower=self.user2, recipient=self.user1)
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.notification_type, 'unfollow')
        self.assertEqual(notification.follower, self.user2)
        self.assertEqual(notification.message,
                         'user2 has unfollowed you.')
