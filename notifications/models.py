from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group
from posts.models import Post
from polymorphic.models import PolymorphicModel

User = get_user_model()
# Create your models here.


class Notification(PolymorphicModel):
    TYPE_CHOICES = (
        ('follow', 'Follow'),
        ('unfollow', 'Unfollow'),
        ('comment', 'Comment'),
        ('join_group', 'Join Group'),
        ('leave_group', 'Leave Group'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return f"{self.recipient.username}'s notification"


class CommentNotification(Notification):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class GroupNotification(Notification):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class FollowNotification(Notification):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
