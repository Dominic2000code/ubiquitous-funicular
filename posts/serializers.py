from rest_framework import serializers
from .models import Post, TextPost, ImagePost, VideoPost, Repost
import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT, db=settings.REDIS_DB)


class TextPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextPost
        fields = ['id', 'author', 'created_at', 'content']


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['id', 'author', 'created_at', 'image']


class VideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPost
        fields = ['id', 'author', 'created_at', 'video']


class PostSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ['polymorphic_ctype']

    def get_content_object(self, obj):
        if isinstance(obj, TextPost):
            serializer = TextPostSerializer(obj)
        elif isinstance(obj, ImagePost):
            serializer = ImagePostSerializer(obj)
        elif isinstance(obj, VideoPost):
            serializer = VideoPostSerializer(obj)
        else:
            serializer = None
        return serializer.data if serializer else None

    def get_likes_count(self, obj):
        return r.zscore('post:likes_count', obj.id) or 0


class RepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repost
        fields = '__all__'
