import os
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from posts.models import Post, TextPost, ImagePost, VideoPost, Repost, Reply, Comment
from posts.serializers import (
    TextPostSerializer, ImagePostSerializer, VideoPostSerializer,
    PostSerializer, RepostSerializer, CommentSerializer, ReplySerializer
)
from django.db.models import F, Count
from django.db.models.functions import Coalesce
from django.db.models import Subquery, OuterRef
from ..permissions import IsAuthorOrReadOnly
import redis
from django.conf import settings
from django.contrib.auth import get_user_model
from ..utils import PostPrivacyMixin
from ..recommendation.recommendation import recommend_posts
from django.db.models import Q
from notifications.notification import create_comment_notification

User = get_user_model()

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT, db=settings.REDIS_DB)


class TextPostCreateView(generics.ListCreateAPIView):
    queryset = TextPost.objects.all()
    serializer_class = TextPostSerializer
    permission_classes = [IsAuthenticated]


class TextPostDetailView(PostPrivacyMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = TextPost.objects.all()
    serializer_class = TextPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()

        check = self.check_privacy(request, post)

        if check['bool_val']:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"detail": check['msg']}, status=status.HTTP_403_FORBIDDEN)


class ImagePostCreateView(generics.ListCreateAPIView):
    queryset = ImagePost.objects.all()
    serializer_class = ImagePostSerializer
    permission_classes = [IsAuthenticated]


class ImagePostDetailView(PostPrivacyMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = ImagePost.objects.all()
    serializer_class = ImagePostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()

        check = self.check_privacy(request, post)

        if check['bool_val']:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"detail": check['msg']}, status=status.HTTP_403_FORBIDDEN)


class VideoPostCreateView(generics.ListCreateAPIView):
    queryset = VideoPost.objects.all()
    serializer_class = VideoPostSerializer
    permission_classes = [IsAuthenticated]


class VideoPostDetailView(PostPrivacyMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoPost.objects.all()
    serializer_class = VideoPostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()

        check = self.check_privacy(request, post)

        if check['bool_val']:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"detail": check['msg']}, status=status.HTTP_403_FORBIDDEN)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class PostDetailView(PostPrivacyMixin, generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()

        check = self.check_privacy(request, post)

        if check['bool_val']:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"detail": check['msg']}, status=status.HTTP_403_FORBIDDEN)


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


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post_instance = get_object_or_404(Post, id=post_id)
        return post_instance.comments.all()

    def perform_create(self, serializer):
        user = self.request.user
        post_id = self.kwargs['post_id']
        post_instance = get_object_or_404(Post, id=post_id)
        create_comment_notification(sender=user, post=post_instance)
        serializer.save(author=user)
        post_instance.comments.add(serializer.instance)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post_id = self.kwargs['post_id']
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(
            Comment, id=comment_id,  post_comments__id=post_id)
        return comment


class ReplyListCreateView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        comment = get_object_or_404(Comment, id=comment_id)
        return comment.replies.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment_id = self.kwargs['comment_id']
        reply_id = self.kwargs['pk']
        reply = get_object_or_404(
            Reply, id=reply_id,  parent_comment_id=comment_id)
        return reply


class IncrementViewsCount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            post.views_count += 1
            post.save()
            return Response({"detail": "ok"}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class TrendingPopularPosts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        likes_count_subquery = User.objects.filter(
            liked_posts=OuterRef('pk')
        ).annotate(likes_count=Count('liked_posts')).values('likes_count')[:1]

        comments_count_subquery = Comment.objects.filter(
            post_comments=OuterRef('pk')
        ).annotate(comments_count=Count('post_comments')).values('comments_count')[:1]

        queryset = Post.objects.annotate(
            total_activity=F('views_count') + F('repost_count') + Coalesce(Subquery(
                likes_count_subquery), 0) + Coalesce(Subquery(comments_count_subquery), 0)
        ).order_by('-total_activity')[:10]

        return queryset


class RecommendationView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Specify the correct path to the recommendation.py file
        recommendation_path = os.path.join(
            settings.BASE_DIR, 'api', 'recommendation', 'recommendation.py')
        # Execute the recommendation logic
        exec(open(recommendation_path).read())

        recommender_posts = recommend_posts(user_id)
        post_ids = recommender_posts['post_id']
        # Fetch all recommended posts in a single query
        recommended_posts_queryset = Post.objects.filter(
            ~Q(author=user_id), id__in=post_ids)
        recommended_posts = PostSerializer(
            recommended_posts_queryset, many=True)

        return Response({"recommended_posts": recommended_posts.data}, status=status.HTTP_200_OK)
