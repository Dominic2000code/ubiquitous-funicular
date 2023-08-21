from rest_framework import serializers
from .models import CustomUser, Follow


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'age', 'profile_picture', 'bio']


class FollowSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['user', 'follower', 'created_at', 'followers_count']

    def get_followers_count(self, obj):
        return Follow.get_follower_count(obj.user_id)
