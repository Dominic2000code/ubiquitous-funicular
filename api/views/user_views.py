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


class FollowerListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        followers = cache.get(f'followers_{user_id}')

        if followers is None:
            followers = Follow.objects.filter(user=user_id)
            cache.set(f'followers_{user_id}', followers)

        follower_ids = followers.values_list('follower_id', flat=True)
        return User.objects.filter(id__in=follower_ids)
