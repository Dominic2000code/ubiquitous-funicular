from django.test import TestCase
from .models import CustomUser


class CustomUserModelTest(TestCase):

    def setUp(self):
        # Create a sample CustomUser instance
        self.user = CustomUser.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            age=25,
            bio='Test bio'
        )

    def test_custom_user_creation(self):
        """Test user creation"""
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(str(self.user), 'testuser')

    def test_custom_user_fields(self):
        """Test fields on user"""
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.age, 25)
        self.assertEqual(self.user.bio, 'Test bio')
        self.assertEqual(str(self.user.profile_picture), '')
