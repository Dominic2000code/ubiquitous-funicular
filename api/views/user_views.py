from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser, Follow
from users.serializers import CustomUserSerializer, FollowSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from ..permissions import IsOwnerOrReadOnly
import redis

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT, db=settings.REDIS_DB)

User = get_user_model()


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class CustomUserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()

        if user.profile_visibility == CustomUser.ProfileVisibilityChoices.PUBLIC:
            return super().retrieve(request, *args, **kwargs)

        elif user.profile_visibility == CustomUser.ProfileVisibilityChoices.FRIENDS_ONLY:
            if request.user.pk in [follow_obj.follower.pk for follow_obj in user.following.all()]:
                return super().retrieve(request, *args, **kwargs)
            else:
                return Response({"detail": "This profile is visible to friends only."}, status=status.HTTP_403_FORBIDDEN)

        # Check if the post is private and the request user is the author
        elif user.profile_visibility == CustomUser.ProfileVisibilityChoices.PRIVATE:
            if request.user.pk == user.pk:
                return super().retrieve(request, *args, **kwargs)
            else:
                return Response({"detail": "This profile is private."}, status=status.HTTP_403_FORBIDDEN)


class ToggleFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        follower = request.user

        if user == follower:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follow_instance = Follow.objects.get(user=user, follower=follower)
            follow_instance.delete()

            # Decrement follower count in Redis
            r.zincrby('user:follower_count', -1, user_id)

            # Decrement following count in Redis for the follower user
            r.zincrby('user:following_count', -1, follower.id)

            return Response({'detail': f'You have unfollowed {user.username}.'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            serializer = FollowSerializer(
                data={'user': user_id, 'follower': follower.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Increment follower count in Redis
            r.zincrby('user:follower_count', 1, user_id)

            # Increment following count in Redis for the follower user
            r.zincrby('user:following_count', 1, follower.id)

            return Response({'detail': f'You are now following {user.username}.'}, status=status.HTTP_201_CREATED)


class FollowerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        if not settings.TESTING:
            cached_data = cache.get(f'followers_data_{user_id}')
            if cached_data:
                return Response(cached_data)

        user = get_object_or_404(CustomUser, id=user_id)
        followers = Follow.objects.filter(user=user)
        follower_ids = followers.values_list('follower_id', flat=True)
        follower_users = CustomUser.objects.filter(id__in=follower_ids)
        follower_data = []
        total_followers_count = Follow.get_follower_count(user.id)

        for follower in follower_users:
            data = {
                'follower': CustomUserSerializer(follower).data,
                'followed_at': followers.get(follower=follower).created_at,
                'followers_count': Follow.get_follower_count(follower.id)
            }
            follower_data.append(data)

        response_data = {
            'followers': follower_data,
            'followers_count': total_followers_count
        }
        if not settings.TESTING:
            cache.set(f'followers_data_{user_id}', response_data, 3600)

        return Response(response_data)


class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if not settings.TESTING:
            cached_data = cache.get(f'following_data_{user_id}')
            if cached_data:
                return Response(cached_data)

        user = get_object_or_404(CustomUser, id=user_id)
        following = Follow.objects.filter(follower=user)
        following_user_ids = following.values_list('user_id', flat=True)
        following_users = CustomUser.objects.filter(id__in=following_user_ids)

        following_data = []
        total_following_count = Follow.get_following_count(user.id)

        for following_user in following_users:
            data = {
                'following_user': CustomUserSerializer(following_user).data,
                'followed_at': following.get(user=following_user).created_at,
                'following_count': Follow.get_following_count(following_user.id),
                'followers_count': Follow.get_follower_count(following_user.id)
            }
            following_data.append(data)

        response_data = {
            'following': following_data,
            'following_count': total_following_count
        }
        if not settings.TESTING:
            cache.set(f'following_data_{user_id}', response_data, 3600)

        return Response(response_data)
