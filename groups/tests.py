from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Group, Membership, GroupPost

User = get_user_model()


class GroupModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.group = Group.objects.create(
            name='Test Group', description='This is a test group', creator=self.user
        )
        Membership.objects.create(user=self.user, group=self.group)

    def test_group_str(self):
        self.assertEqual(str(self.group), f'Group owner: {self.group.name}')

    def test_membership_created(self):
        membership = Membership.objects.get(user=self.user, group=self.group)
        self.assertIsNotNone(membership)

    def test_group_has_member(self):
        self.assertIn(self.user, self.group.members.all())


class GroupPostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.group = Group.objects.create(
            name='Test Group', description='This is a test group',
            creator=self.user)
        self.group_post = GroupPost.objects.create(
            group=self.group, author=self.user, content='Test content')

    def test_group_post_str(self):
        self.assertEqual(
            str(self.group_post),
            f'Group Post by {self.user} in {self.group}'
        )

    def test_group_post_has_content(self):
        self.assertEqual(self.group_post.content, 'Test content')
