from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from groups.models import Group, Membership, GroupPost
from django.urls import reverse

User = get_user_model()


class GroupViewsTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="password1")
        self.user2 = User.objects.create_user(
            username="user2", password="password2")

    def create_group(self, name="Test Group", description="Test Description"):
        return Group.objects.create(name=name, description=description, creator=self.user1)

    def test_create_group(self):
        self.client.force_authenticate(self.user1)
        url = reverse('api:group-list-create')
        data = {
            "name": "New Group",
            "description": "New Description"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Group.objects.count(), 1)

    def test_join_group(self):
        group = self.create_group()
        self.client.force_authenticate(self.user2)
        url = reverse('api:join-group', args=[group.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(group.members.count(), 1)

    def test_leave_group(self):
        group = self.create_group()
        Membership.objects.create(user=self.user2, group=group)
        self.client.force_authenticate(self.user2)
        url = reverse('api:leave-group', args=[group.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(group.members.count(), 0)

    def test_delete_group(self):
        group = self.create_group()
        self.client.force_authenticate(self.user1)
        url = reverse('api:delete-group', args=[group.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Group.objects.count(), 0)

    def test_kick_member(self):
        group = self.create_group()
        Membership.objects.create(user=self.user2, group=group)
        self.client.force_authenticate(self.user1)
        url = reverse('api:kick-member', args=[group.id, self.user2.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(group.members.count(), 0)

    def test_create_group_post(self):
        group = self.create_group()
        Membership.objects.create(user=self.user1, group=group)
        self.client.force_authenticate(self.user1)
        url = reverse('api:group-post-list')
        data = {
            "group": group.id,
            "content": "Hello, Group!",
            "author": self.user1.id
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(GroupPost.objects.count(), 1)

    def test_get_group_post(self):
        group = self.create_group()
        Membership.objects.create(user=self.user1, group=group)
        post = GroupPost.objects.create(
            group=group, author=self.user1, content="Hello, Group!")
        self.client.force_authenticate(self.user1)
        url = reverse('api:group-post-detail', args=[post.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_group_post(self):
        group = self.create_group()
        Membership.objects.create(user=self.user1, group=group)
        post = GroupPost.objects.create(
            group=group, author=self.user1, content="Hello, Group!")
        update_data = {
            "content": "Updated content"
        }
        self.client.force_authenticate(self.user1)
        url = reverse('api:group-post-detail', args=[post.id])
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_data["content"], response.data['content'])

    def test_delete_group_post(self):
        group = self.create_group()
        Membership.objects.create(user=self.user1, group=group)
        post = GroupPost.objects.create(
            group=group, author=self.user1, content="Hello, Group!")
        self.client.force_authenticate(self.user1)
        url = reverse('api:group-post-detail', args=[post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
