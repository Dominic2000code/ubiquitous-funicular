from rest_framework import serializers
from .models import Group, Membership, GroupPost


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class GroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPost
        fields = '__all__'
