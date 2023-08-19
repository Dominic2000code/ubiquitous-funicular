from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.username
