from rest_framework import serializers
from .models import Post, TextPost, ImagePost, VideoPost


class TextPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextPost
        fields = '__all__'


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = '__all__'


class VideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPost
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

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
