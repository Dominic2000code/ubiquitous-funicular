from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    get:
    Return all notifications for specified user_id
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Notification.objects.filter(recipient_id=user_id)


class NotificationMarkReadView(APIView):
    """
    patch:
    Mark notification as read for specified notification
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')
        try:
            notification = Notification.objects.get(pk=notification_id)
        except Notification.DoesNotExist:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read'}, status=status.HTTP_200_OK)
