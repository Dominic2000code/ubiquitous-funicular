from rest_framework import serializers
from .models import FollowNotification, CommentNotification, GroupNotification, Notification


class FollowNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowNotification
        exclude = ['polymorphic_ctype']


class CommentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentNotification
        exclude = ['polymorphic_ctype']


class GroupNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupNotification
        exclude = ['polymorphic_ctype']


class NotificationSerializer(serializers.ModelSerializer):
    notification = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['notification']

    def get_notification(self, obj):
        if isinstance(obj, FollowNotification):
            serializer = FollowNotificationSerializer(obj)
        elif isinstance(obj, CommentNotification):
            serializer = CommentNotificationSerializer(obj)
        elif isinstance(obj, GroupNotification):
            serializer = GroupNotificationSerializer(obj)
        else:
            serializer = None
        return serializer.data if serializer else None
