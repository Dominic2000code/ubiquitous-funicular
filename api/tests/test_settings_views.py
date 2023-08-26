from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from posts.models import TextPost
from django.contrib.auth import get_user_model

User = get_user_model()


class ChangePostPrivacyLevelViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.text_post = TextPost.objects.create(
            author=self.user, content="Test content", privacy_level="public"
        )
        self.url = reverse(
            "api:change-privacy-level",
            args=[self.text_post.pk]
        )
        self.profile_visibility_url = reverse(
            "api:change-profile-visibility",
            args=[self.user.pk]
        )

    def test_change_privacy_level_public(self):
        response = self.client.patch(
            self.url, data={"privacy_level": "public"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["detail"], "Privacy level updated successfully."
        )
        self.text_post.refresh_from_db()
        self.assertEqual(self.text_post.privacy_level, "public")

    def test_change_privacy_level_friends_only(self):
        response = self.client.patch(
            self.url, data={"privacy_level": "friends_only"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["detail"], "Privacy level updated successfully."
        )
        self.text_post.refresh_from_db()
        self.assertEqual(self.text_post.privacy_level, "friends_only")

    def test_change_privacy_level_private(self):
        response = self.client.patch(
            self.url, data={"privacy_level": "private"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["detail"], "Privacy level updated successfully."
        )
        self.text_post.refresh_from_db()
        self.assertEqual(self.text_post.privacy_level, "private")

    def test_change_privacy_level_invalid(self):
        response = self.client.patch(
            self.url, data={"privacy_level": "invalid_privacy"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "Invalid privacy level.")

    def test_change_privacy_level_missing_field(self):
        response = self.client.patch(self.url, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["detail"], "Privacy level field is required."
        )

    def test_change_profile_visibility_level_public(self):
        response = self.client.patch(
            self.profile_visibility_url, data={"profile_visibility_level": "public"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["detail"], "Visibility level updated successfully."
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_visibility, "public")

    def test_change_profile_visibility_level_friends_only(self):
        response = self.client.patch(
            self.profile_visibility_url, data={
                "profile_visibility_level": "friends_only"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["detail"], "Visibility level updated successfully."
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_visibility, "friends_only")

    def test_change_profile_visibility_level_private(self):
        response = self.client.patch(
            self.profile_visibility_url, data={"profile_visibility_level": "private"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["detail"], "Visibility level updated successfully."
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_visibility, "private")

    def test_change_profile_visibility_level_invalid(self):
        response = self.client.patch(
            self.profile_visibility_url, data={
                "profile_visibility_level": "invalid_privacy"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "Invalid visibility level.")

    def test_change_profile_visibility_level_missing_field(self):
        response = self.client.patch(self.profile_visibility_url, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["detail"], "Visibility level field is required."
        )
