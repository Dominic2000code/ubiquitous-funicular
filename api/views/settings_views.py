from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posts.models import Post


class ChangePostPrivacyLevelView(APIView):
    """
    Make a patch request with privacy_level set to (public,private or friends_only). 
    eg. {
            "privacy_level" : "friends_only"
        }
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        new_privacy_level = request.data.get("privacy_level")
        if new_privacy_level:
            if new_privacy_level in ['public', 'friends_only', 'private']:
                post.privacy_level = new_privacy_level
                post.save()
                return Response({"detail": "Privacy level updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid privacy level."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Privacy level field is required."}, status=status.HTTP_400_BAD_REQUEST)
