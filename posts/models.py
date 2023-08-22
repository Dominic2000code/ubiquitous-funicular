from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(PolymorphicModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    repost_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.author}'s post {self.id}"


class Repost(models.Model):
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'original_post')

    def __str__(self) -> str:
        return f"Repost of {self.original_post.author}'s post by {self.user}"


class TextPost(Post):
    content = models.TextField()

    def __str__(self):
        return f"{self.author}'s text post"


class ImagePost(Post):
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"{self.author}'s image post"


class VideoPost(Post):
    video = models.FileField(upload_to='post_videos/')

    def __str__(self):
        return f"{self.author}'s video post"
