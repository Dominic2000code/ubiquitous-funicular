from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, TextPost, ImagePost, VideoPost
from posts.serializers import TextPostSerializer, ImagePostSerializer, VideoPostSerializer, PostSerializer


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
