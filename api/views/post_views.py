from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, TextPost, ImagePost, VideoPost
from posts.serializers import TextPostSerializer, ImagePostSerializer, VideoPostSerializer, PostSerializer
import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT, db=settings.REDIS_DB)


class TextPostCreateView(generics.ListCreateAPIView):
    queryset = TextPost.objects.all()
    serializer_class = TextPostSerializer
    permission_classes = [IsAuthenticated]


class TextPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TextPost.objects.all()
    serializer_class = TextPostSerializer
    permission_classes = [IsAuthenticated]


class ImagePostCreateView(generics.ListCreateAPIView):
    queryset = ImagePost.objects.all()
    serializer_class = ImagePostSerializer
    permission_classes = [IsAuthenticated]


class ImagePostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImagePost.objects.all()
    serializer_class = ImagePostSerializer
    permission_classes = [IsAuthenticated]


class VideoPostCreateView(generics.ListCreateAPIView):
    queryset = VideoPost.objects.all()
    serializer_class = VideoPostSerializer
    permission_classes = [IsAuthenticated]


class VideoPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoPost.objects.all()
    serializer_class = VideoPostSerializer
    permission_classes = [IsAuthenticated]


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            # Decrease the like count in Redis
            r.zincrby('post:likes_count', -1, post_id)
            return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            # Increase the like count in Redis
            r.zincrby('post:likes_count', 1, post_id)
            return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
