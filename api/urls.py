from django.urls import path
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
                    ReplyListCreateView, SearchView,
                    UserSearchView, GroupSearchView, PostSearchView,
                    IncrementViewsCount, TrendingPopularPosts,
                    ChangePostPrivacyLevelView, ChangeProfileVisibilityView,
                    RecommendationView, NotificationMarkReadView, NotificationListView)

app_name = 'api'


urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),

    path('users/toggle-follow/<int:user_id>/',
         ToggleFollowView.as_view(), name='toggle-follow'),

    path('users/followers/<int:user_id>/',
         FollowerListView.as_view(), name='follower-list'),
    path('users/following/<int:user_id>/',
         FollowingListView.as_view(), name='following-list'),

    path('users/<int:user_id>/change-profile-visibility/',
         ChangeProfileVisibilityView.as_view(), name='change-profile-visibility'),

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
    path('posts/<int:post_id>/increment-views/',
         IncrementViewsCount.as_view(), name='increment-views'),
    path('posts/trending-popular/', TrendingPopularPosts.as_view(),
         name='trending-popular-posts'),

    path('posts/recommendation/<int:user_id>/',
         RecommendationView.as_view(), name='recommend-posts'),

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

    path('posts/<int:post_id>/change-privacy/',
         ChangePostPrivacyLevelView.as_view(), name='change-privacy-level'),

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

    path('search/', SearchView.as_view(), name='search'),
    path('search/users/', UserSearchView.as_view(), name='user-search'),
    path('search/posts/', PostSearchView.as_view(), name='post-search'),
    path('search/groups/', GroupSearchView.as_view(), name='group-search'),

    path('notifications/<int:user_id>/',
         NotificationListView.as_view(), name='user-notifications'),
    path('notifications/mark-read/<int:pk>/',
         NotificationMarkReadView.as_view(), name='mark-notification-read'),
]
