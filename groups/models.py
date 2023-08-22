from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(
        User, related_name='groups_joined', through='Membership')
    creator = models.ForeignKey(
        User, related_name='created_groups', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Group owner: {self.name}'


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, related_name='memberships', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)


class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='group_posts_images/', blank=True, null=True)
    video = models.FileField(
        upload_to='group_posts_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Group Post by {self.author} in {self.group}"
