from rest_framework import serializers
from .models import Post, TextPost, ImagePost, VideoPost, Repost, Comment, Reply
import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT, db=settings.REDIS_DB)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TextPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = TextPost
        fields = ['id', 'author', 'created_at',
                  'content', 'likes', 'views_count']

    def get_likes(self, obj):
        return r.zscore('post:likes_count', obj.id) or 0


class ImagePostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = ImagePost
        fields = ['id', 'author', 'created_at',
                  'image', 'likes', 'views_count']

    def get_likes(self, obj):
        return r.zscore('post:likes_count', obj.id) or 0


class VideoPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = VideoPost
        fields = ['id', 'author', 'created_at',
                  'video', 'likes', 'views_count']

    def get_likes(self, obj):
        return r.zscore('post:likes_count', obj.id) or 0


class PostSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        exclude = ['polymorphic_ctype']

    def get_post(self, obj):
        if isinstance(obj, TextPost):
            serializer = TextPostSerializer(obj)
        elif isinstance(obj, ImagePost):
            serializer = ImagePostSerializer(obj)
        elif isinstance(obj, VideoPost):
            serializer = VideoPostSerializer(obj)
        else:
            serializer = None
        return serializer.data if serializer else None

    def get_likes(self, obj):
        return r.zscore('post:likes_count', obj.id) or 0


class RepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repost
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'
