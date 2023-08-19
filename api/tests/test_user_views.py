from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from rest_framework.authtoken.models import Token


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
        self.client.force_authenticate(self.user)

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