from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.auth import get_user_model


class Post(PolymorphicModel):
    User = get_user_model()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}'s post {self.id}"


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
