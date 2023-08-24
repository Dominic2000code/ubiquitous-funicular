from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from posts.models import TextPost
from groups.models import Group
from users.serializers import CustomUserSerializer
from posts.serializers import TextPostSerializer
from groups.serializers import GroupSerializer


User = get_user_model()


class SearchView(generics.ListAPIView):
    serializer_classes = {
        'users': CustomUserSerializer,
        'posts': TextPostSerializer,
        'groups': GroupSerializer,
    }

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        users = User.objects.filter(Q(username__icontains=query) | Q(
            first_name__icontains=query) | Q(last_name__icontains=query))
        posts = TextPost.objects.filter(content__icontains=query)
        groups = Group.objects.filter(name__icontains=query)
        return {
            'users': users,
            'posts': posts,
            'groups': groups,
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = {
            entity: self.serializer_classes[entity](queryset[entity], many=True).data for entity in queryset
        }
        return Response(serialized_data)


class UserSearchView(generics.ListAPIView):
    queryset = CustomUserSerializer
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))


class PostSearchView(generics.ListAPIView):
    queryset = TextPost
    serializer_class = TextPostSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return TextPost.objects.filter(content__icontains=query)


class GroupSearchView(generics.ListAPIView):
    queryset = Group
    serializer_class = GroupSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Group.objects.filter(name__icontains=query)
