from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, TextPost, ImagePost, VideoPost, Repost
from posts.serializers import TextPostSerializer, ImagePostSerializer, VideoPostSerializer, PostSerializer, RepostSerializer
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
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            # Decrease the like count in Redis
            r.zincrby('post:likes_count', -1, post_id)
            likes_count = r.zscore('post:likes_count', post_id)
        else:
            post.likes.add(user)
            # Increase the like count in Redis
            r.zincrby('post:likes_count', 1, post_id)
            likes_count = r.zscore('post:likes_count', post_id)

        return Response({'likes_count': int(likes_count)}, status=status.HTTP_200_OK)


class RepostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            original_post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound("Original post not found")

        user = request.user

        try:
            repost = Repost.objects.create(
                original_post=original_post, user=user)
            original_post.repost_count += 1
            original_post.save()

            serializer = RepostSerializer(repost)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'detail': 'You have already reposted this post.'}, status=status.HTTP_400_BAD_REQUEST)


class RepostListAPIView(generics.ListAPIView):
    serializer_class = RepostSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Repost.objects.filter(original_post_id=post_id)
