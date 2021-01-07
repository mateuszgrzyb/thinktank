from importlib._common import _

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

from post.models import Post


class User(AbstractUser):
    bio = models.TextField(
        max_length=200,
        null=False,
        blank=True,
    )

    following = models.ManyToManyField(
        'User',
        blank=True,
        symmetrical=False,
        related_name='followers',
    )

    def click_like(self, post_pk: int):
        posts = self.posts_liked_by_user
        if posts.filter(pk=post_pk).exists():
            posts.remove(post_pk)
        else:
            posts.add(post_pk)


def users():
    return User.objects
