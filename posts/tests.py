from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import TextPost, ImagePost, VideoPost, Post, Repost, Comment, Reply
from .serializers import TextPostSerializer, ImagePostSerializer, VideoPostSerializer

User = get_user_model()


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_text_post_creation(self):
        text_post = TextPost.objects.create(
            author=self.user, content='This is a test content.')
        self.assertEqual(str(text_post), f"{self.user}'s text post")

    def test_text_post_serializer(self):
        data = {'author': self.user.id, 'content': 'This is a test content.'}
        serializer = TextPostSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_text_post_serializer_round_trip(self):
        data = {'author': self.user.id, 'content': 'This is a test content.'}
        serializer = TextPostSerializer(data=data)
        serializer.is_valid()
        text_post = serializer.save()

        serialized_data = TextPostSerializer(text_post).data

        expected_data = {
            'id': text_post.id,
            'author': text_post.author.id,
            'content': 'This is a test content.',
        }
        self.assertEqual(serialized_data['id'], expected_data['id'])
        self.assertEqual(serialized_data['author'], expected_data['author'])
        self.assertEqual(serialized_data['content'], expected_data['content'])

    def test_text_post_inheritance(self):
        text_post = TextPost.objects.create(
            author=self.user, content='This is a test content.')
        post = Post.objects.get(id=text_post.id)
        self.assertIsInstance(post, TextPost)

    def test_image_post_creation(self):
        image_post = ImagePost.objects.create(
            author=self.user, image='path/to/test/image.jpg')
        self.assertEqual(str(image_post), f"{self.user}'s image post")

    def test_image_post_serializer(self):
        data = {'author': self.user.id, 'image': 'path/to/test/image.jpg'}
        serializer = ImagePostSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_image_post_inheritance(self):
        image_post = ImagePost.objects.create(
            author=self.user, image='path/to/test/image.jpg')
        post = Post.objects.get(id=image_post.id)
        self.assertIsInstance(post, ImagePost)

    def test_video_post_creation(self):
        video_post = VideoPost.objects.create(
            author=self.user, video='path/to/test/video.mp4')
        self.assertEqual(str(video_post), f"{self.user}'s video post")

    def test_video_post_serializer(self):
        data = {'author': self.user.id, 'video': 'path/to/test/video.mp4'}
        serializer = VideoPostSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_video_post_inheritance(self):
        video_post = VideoPost.objects.create(
            author=self.user, video='path/to/test/video.mp4')
        post = Post.objects.get(id=video_post.id)
        self.assertIsInstance(post, VideoPost)

    def test_model_likes(self):
        """Test adding likes to the model"""
        post = TextPost.objects.create(
            author=self.user, content='Test post content.')
        self.assertEqual(post.likes.count(), 0)
        post.likes.add(self.user)
        self.assertEqual(post.likes.count(), 1)

    def test_repost_creation(self):
        text_post = TextPost.objects.create(
            author=self.user, content='This is a test content.')
        repost = Repost.objects.create(
            original_post=text_post, user=self.user)
        self.assertEqual(
            str(repost), f"Repost of {text_post.author}'s post by {self.user}")

    def test_create_comment(self):
        comment = Comment.objects.create(
            author=self.user,
            content='This is a comment.'
        )
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'This is a comment.')

    def test_create_reply(self):
        comment = Comment.objects.create(
            author=self.user,
            content='This is a comment.'
        )
        reply = Reply.objects.create(
            author=self.user,
            content='This is a reply.',
            parent_comment=comment
        )
        self.assertEqual(reply.author, self.user)
        self.assertEqual(reply.content, 'This is a reply.')
        self.assertEqual(reply.parent_comment, comment)
