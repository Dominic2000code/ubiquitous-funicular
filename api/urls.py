from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomUserDetailView, CustomUserListCreateView,
                    TextPostCreateView, TextPostDetailView,
                    ImagePostCreateView, ImagePostDetailView,
                    VideoPostCreateView, VideoPostDetailView,
                    PostListView, PostDetailView,)

app_name = 'api'

router = DefaultRouter()


urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),

    path('text-posts/', TextPostCreateView.as_view(),
         name='textpost-list-create'),
    path('text-posts/<int:pk>/', TextPostDetailView.as_view(),
         name='textpost-detail'),

    path('image-posts/', ImagePostCreateView.as_view(),
         name='imagepost-list-create'),
    path('image-posts/<int:pk>/', ImagePostDetailView.as_view(),
         name='imagepost-detail'),

    path('video-posts/', VideoPostCreateView.as_view(),
         name='videopost-list-create'),
    path('video-posts/<int:pk>/', VideoPostDetailView.as_view(),
         name='videopost-detail'),

    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
