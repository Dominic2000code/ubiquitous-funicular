from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from groups.models import Group, Membership, GroupPost
from groups.serializers import GroupSerializer, MembershipSerializer, GroupPostSerializer
from groups.permissions import IsGroupCreator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save(creator=self.request.user)
        group.members.add(self.request.user)


class JoinLeaveGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        user = request.user
        group = Group.objects.get(pk=group_id)

        if 'join' in request.path:
            if group.members.filter(id=user.id).exists():
                return Response({"detail": "You are already a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

            Membership.objects.create(user=user, group=group)
            return Response({"detail": f"You have joined the group {group.name}."}, status=status.HTTP_201_CREATED)

        elif 'leave' in request.path:
            try:
                membership = Membership.objects.get(user=user, group=group)
                membership.delete()
                return Response({"detail": f"You have left the group {group.name}."}, status=status.HTTP_200_OK)
            except Membership.DoesNotExist:
                raise NotFound("You are not a member of this group.")

        return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


class GroupDeleteView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsGroupCreator]


class KickMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id, user_id):
        user = request.user
        group = Group.objects.get(pk=group_id)

        if group.creator != user:
            raise PermissionDenied("You are not the creator of this group.")

        try:
            member = Membership.objects.get(user_id=user_id, group=group)
            member.delete()
            return Response({"detail": f"Member has been kicked out from the group."}, status=status.HTTP_200_OK)
        except Membership.DoesNotExist:
            raise NotFound("The specified user is not a member of this group.")


class GroupPostListCreateView(generics.ListCreateAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.validated_data['group']

        if not group.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You are not a member of this group.")
        serializer.save(author=self.request.user)


class GroupPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        group_post = super().get_object()
        group = group_post.group

        if not group.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You are not a member of this group.")

        return group_post

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied(
                "You don't have permission to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied(
                "You don't have permission to delete this post.")
        instance.delete()
