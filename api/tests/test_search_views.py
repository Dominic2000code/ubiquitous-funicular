from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import TextPost
from groups.models import Group
from users.serializers import CustomUserSerializer
from posts.serializers import TextPostSerializer
from groups.serializers import GroupSerializer

User = get_user_model()


class SearchViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)

        self.text_post = TextPost.objects.create(
            author=self.user, content='This is a test content.')
        self.group = Group.objects.create(
            name='Test Group', creator=self.user)

    def test_search_view(self):
        url = reverse('api:search')
        response = self.client.get(url, {'q': 'test'})
        self.assertEqual(response.status_code, 200)

        expected_data = {
            'users': [CustomUserSerializer(self.user).data],
            'posts': [TextPostSerializer(self.text_post).data],
            'groups': [GroupSerializer(self.group).data],
        }
        self.assertEqual(response.data, expected_data)

    def test_user_search_view(self):
        url = reverse('api:user-search')
        response = self.client.get(url, {'q': 'testuser'})
        self.assertEqual(response.status_code, 200)

        expected_data = [CustomUserSerializer(self.user).data]
        self.assertEqual(response.data, expected_data)

    def test_post_search_view(self):
        url = reverse('api:post-search')
        response = self.client.get(url, {'q': 'test'})
        self.assertEqual(response.status_code, 200)

        expected_data = [TextPostSerializer(self.text_post).data]
        self.assertEqual(response.data, expected_data)

    def test_group_search_view(self):
        url = reverse('api:group-search')
        response = self.client.get(url, {'q': 'test'})
        self.assertEqual(response.status_code, 200)

        expected_data = [GroupSerializer(self.group).data]
        self.assertEqual(response.data, expected_data)
