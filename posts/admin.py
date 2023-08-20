from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models import Post, TextPost, ImagePost, VideoPost


class PostChildAdmin(PolymorphicChildModelAdmin):
    base_model = Post  # The parent model


@admin.register(Post)
class PostAdmin(PolymorphicParentModelAdmin):
    base_model = Post  # The parent model
    child_models = (TextPost, ImagePost, VideoPost)


@admin.register(TextPost)
class TextPostAdmin(PostChildAdmin):
    base_model = TextPost
    show_in_index = True


@admin.register(ImagePost)
class ImagePostAdmin(PostChildAdmin):
    base_model = ImagePost
    show_in_index = True


@admin.register(VideoPost)
class VideoPostAdmin(PostChildAdmin):
    base_model = VideoPost
    show_in_index = True
