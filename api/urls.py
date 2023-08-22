from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomUserDetailView, CustomUserListCreateView,
                    TextPostCreateView, TextPostDetailView,
                    ImagePostCreateView, ImagePostDetailView,
                    VideoPostCreateView, VideoPostDetailView,
                    PostListView, PostDetailView,
                    ToggleLikeView, RepostView, RepostListAPIView,
                    FollowerListView, ToggleFollowView,
                    FollowingListView)

app_name = 'api'

router = DefaultRouter()


urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('users/toggle-follow/<int:user_id>/',
         ToggleFollowView.as_view(), name='toggle-follow'),
    path('users/followers/<int:user_id>/',
         FollowerListView.as_view(), name='follower-list'),
    path('users/following/<int:user_id>/',
         FollowingListView.as_view(), name='follower-list'),

    path('posts/text-posts/', TextPostCreateView.as_view(),
         name='textpost-list-create'),
    path('posts/text-posts/<int:pk>/', TextPostDetailView.as_view(),
         name='textpost-detail'),

    path('posts/image-posts/', ImagePostCreateView.as_view(),
         name='imagepost-list-create'),
    path('posts/image-posts/<int:pk>/', ImagePostDetailView.as_view(),
         name='imagepost-detail'),

    path('posts/video-posts/', VideoPostCreateView.as_view(),
         name='videopost-list-create'),
    path('posts/video-posts/<int:pk>/', VideoPostDetailView.as_view(),
         name='videopost-detail'),

    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('posts/toggle-like/<int:post_id>/',
         ToggleLikeView.as_view(), name='toggle-like'),

    path('posts/repost/<int:post_id>/', RepostView.as_view(), name='repost'),
    path('posts/reposts/<int:post_id>/',
         RepostListAPIView.as_view(), name='repost-list'),
]
