import posts
from .models import FollowNotification, CommentNotification, GroupNotification


def create_follow_notification(follower, recipient):
    message = f"{follower.username} has started following you."
    notification = FollowNotification.objects.create(
        recipient=recipient,
        follower=follower,
        notification_type='follow',
        message=message
    )
    return notification


def create_unfollow_notification(follower, recipient):
    message = f"{follower.username} has unfollowed you."
    notification = FollowNotification.objects.create(
        recipient=recipient,
        follower=follower,
        notification_type='unfollow',
        message=message
    )
    return notification


def create_join_group_notification(user, group):
    message = f"{user.username} has joined the group '{group.name}'."
    notification = GroupNotification.objects.create(
        recipient=group.creator,
        notification_type='join_group',
        group=group,
        message=message
    )
    return notification


def create_leave_group_notification(user, group):
    message = f"{user.username} has left the group '{group.name}'."
    notification = GroupNotification.objects.create(
        recipient=group.creator,
        notification_type='leave_group',
        group=group,
        message=message
    )
    return notification


def create_comment_notification(sender, post):
    message = f"{sender.username} has commented on your post."
    notification = CommentNotification.objects.create(
        recipient=post.author,
        notification_type='comment',
        post=post,
        message=message
    )
    return notification
