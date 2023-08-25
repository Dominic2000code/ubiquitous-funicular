from contextlib import contextmanager
from django.conf import settings
from rest_framework.views import APIView
from posts.models import Post


@contextmanager
def set_testing(value):
    original_value = settings.TESTING
    settings.TESTING = value
    yield
    settings.TESTING = original_value


class PostPrivacyMixin(APIView):
    def check_privacy(self, request, post):
        if post.privacy_level == Post.PrivacyChoices.PUBLIC:
            return {"bool_val": True, "msg": ""}

        if post.privacy_level == Post.PrivacyChoices.FRIENDS_ONLY:
            return {"bool_val": request.user.pk in [following_obj.follower.pk for following_obj in post.author.following.all()], "msg": "This post is for friends only."}

        if post.privacy_level == Post.PrivacyChoices.PRIVATE:
            return {"bool_val": request.user == post.author, "msg": "This post is private"}

        return False
