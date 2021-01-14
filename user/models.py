import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from post.models import Post


class PrivRoom(models.Model):
    user1 = models.ForeignKey(
        'User',
        related_name='user1',
        on_delete=models.CASCADE,
    )

    user2 = models.ForeignKey(
        'User',
        related_name='user2',
        on_delete=models.CASCADE,
    )

    url = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        unique_together = ('user1', 'user2')

    def can_be_entered_by(self, user) -> bool:
        return user.pk == self.user1.pk or user.pk == self.user2.pk


def priv_rooms():
    return PrivRoom.objects.all()


class User(AbstractUser):
    bio = models.TextField(
        max_length=200,
        null=False,
        blank=True,
    )

    following = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='followers',
    )

    priv_chats = models.ManyToManyField(
        'self',
        symmetrical=False,
        through=PrivRoom,
    )

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


class Message(models.Model):
    body = models.TextField()

    room = models.ForeignKey(
        PrivRoom,
        on_delete=models.CASCADE
    )

    time_created = models.DateTimeField(
        auto_now_add=True
    )
