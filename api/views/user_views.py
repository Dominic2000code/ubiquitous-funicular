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
    permission_classes = [IsAuthenticated]


class ToggleFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        follower = request.user

        try:
            follow_instance = Follow.objects.get(user=user, follower=follower)
            follow_instance.delete()

            # Decrement follower count in Redis
            r.zincrby('user:follower_count', -1, user_id)

            return Response({'detail': f'You have unfollowed {user.username}.'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            serializer = FollowSerializer(
                data={'user': user_id, 'follower': follower.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Increment follower count in Redis
            r.zincrby('user:follower_count', 1, user_id)

            return Response({'detail': f'You are now following {user.username}.'}, status=status.HTTP_201_CREATED)


class FollowerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
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
        cache.set(f'followers_data_{user_id}', response_data, 3600)

        return Response(response_data)
