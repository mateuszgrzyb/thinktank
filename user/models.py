from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from post.models import Post
from post.models import posts


class User(AbstractUser):

    def click_like(self, post_pk: int):
        posts = self.posts_liked_by_user
        if posts.filter(pk=post_pk).exists():
            posts.remove(post_pk)
        else:
            posts.add(post_pk)


def users():
    return User.objects
