from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomUserDetailView, CustomUserListCreateView,
                    TextPostCreateView, TextPostDetailView,
                    ImagePostCreateView, ImagePostDetailView,
                    VideoPostCreateView, VideoPostDetailView,
                    PostListView, PostDetailView,
                    ToggleLikeView, RepostView, RepostListAPIView,
                    FollowerListView, ToggleFollowView,
                    FollowingListView, GroupListCreateView,
                    JoinLeaveGroupView, GroupDeleteView,
                    KickMemberView, GroupPostListCreateView,
                    GroupPostDetailView, CommentDetailView,
                    CommentListCreateView, ReplyDetailView,
                    ReplyListCreateView)

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
         FollowingListView.as_view(), name='following-list'),

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

    path('posts/<int:post_id>/comments/',
         CommentListCreateView.as_view(), name='post-comment-list'),
    path('posts/<int:post_id>/comments/<int:pk>/',
         CommentDetailView.as_view(), name='post-comment-detail'),
    path('posts/comments/<int:comment_id>/replies/',
         ReplyListCreateView.as_view(), name='comment-reply-list'),
    path('posts/comments/<int:comment_id>/replies/<int:pk>/',
         ReplyDetailView.as_view(), name='comment-reply-detail'),

    path('groups/', GroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:group_id>/join/',
         JoinLeaveGroupView.as_view(), name='join-group'),
    path('groups/<int:group_id>/leave/',
         JoinLeaveGroupView.as_view(), name='leave-group'),
    path('groups/<int:pk>/delete/',
         GroupDeleteView.as_view(), name='delete-group'),
    path('groups/<int:group_id>/kick/<int:user_id>/',
         KickMemberView.as_view(), name='kick-member'),

    path('groups/posts/', GroupPostListCreateView.as_view(), name='group-post-list'),
    path('groups/post/<int:pk>/', GroupPostDetailView.as_view(),
         name='group-post-detail'),
]
