
from django.contrib.auth.models import AbstractUser
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

    # def click_like(self, post_pk: int):
    #     posts = self.posts_liked_by_user
    #     if posts.filter(pk=post_pk).exists():
    #         posts.remove(post_pk)
    #     else:
    #         posts.add(post_pk)
    #
    # def click_follow(self, user_pk: int):
    #     _users = self.following
    #     if _users.filter(pk=user_pk).exists():
    #         _users.remove(user_pk)
    #     else:
    #         _users.add(user_pk)

    def add_or_remove(self, pk: int, group):
        if group.filter(pk=pk).exists():
            group.remove(pk)
        else:
            group.add(pk)

    def click_like(self, post_pk: int):
        self.add_or_remove(post_pk, self.posts_liked_by_user)

    def click_follow(self, user_pk: int):
        self.add_or_remove(user_pk, self.following)


def users():
    return User.objects
