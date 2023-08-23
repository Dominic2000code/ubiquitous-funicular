from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser, Follow
from users.serializers import CustomUserSerializer
from django.conf import settings
from django.test import override_settings
from ..utils import set_testing
import redis


@override_settings(REDIS_DB=settings.TEST_REDIS_DB)
class CustomUserViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testUser',
            'first_name': 'Test',
            'last_name': 'User',
            'age': 25,
            'bio': 'Test bio'
        }
        self.user = CustomUser.objects.create(**self.user_data)
        self.follower = CustomUser.objects.create(
            username='testFollower',
            first_name='Test',
            last_name='Follower',
            age=25,
            bio='Test Follower bio'
        )
        self.client.force_authenticate(self.user)
        self.r = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def tearDown(self):
        self.r.zrem('user:follower_count', self.user.id)

    def test_create_user(self):
        """Test user creation"""
        data = self.user_data
        data['username'] = 'test'
        response = self.client.post(
            reverse('api:user-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users(self):
        """List all users in db"""
        response = self.client.get(reverse('api:user-list-create'))
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        """Retrieve a single user from db """
        response = self.client.get(
            reverse('api:user-detail', args=[self.user.id]))
        user = CustomUser.objects.get(id=self.user.id)
        serializer = CustomUserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        """Update fields of a user"""
        updated_data = {
            'username': 'Updated_username',
            'first_name': 'Updated',
            'last_name': 'User',
            'age': 30,
            'bio': 'Updated bio'
        }
        response = self.client.put(
            reverse('api:user-detail', args=[self.user.id]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, updated_data['first_name'])
        self.assertEqual(user.age, updated_data['age'])

    def test_toggle_follow(self):
        url = reverse('api:toggle-follow', args=[self.follower.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # Follow

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Unfollow

    def test_follower_list_view(self):
        follow = Follow.objects.create(user=self.user, follower=self.follower)
        url = reverse('api:follower-list', args=[self.user.id])

        with set_testing(True):  # Temporarily set TESTING to True
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['followers']), 1)
            self.assertEqual(
                response.data['followers'][0]['follower']['username'],
                self.follower.username
            )

    def test_following_list_view(self):
        follow = Follow.objects.create(user=self.user, follower=self.follower)
        url = reverse('api:following-list', args=[self.follower.id])

        with set_testing(True):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['following']), 1)
            self.assertEqual(
                response.data['following'][0]['following_user']['username'],
                self.user.username
            )
