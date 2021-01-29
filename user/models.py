import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import Q

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

    def __str__(self):
        return f'{self.user1}: {self.user2}'


def priv_rooms():
    return PrivRoom.objects.all()


def priv_room(u1, u2, default=None):
    try:
        return priv_rooms().get(
            (Q(user1=u1) & Q(user2=u2)) |
            (Q(user1=u2) & Q(user2=u1))
        )
    except PrivRoom.DoesNotExist:
        return default


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

    def add_or_remove(self, pk: int, group) -> None:
        if group.filter(pk=pk).exists():
            group.remove(pk)
        else:
            group.add(pk)

    def click_like(self, post_pk: int) -> None:
        self.add_or_remove(post_pk, self.posts_liked_by_user)

    def click_follow(self, user_pk: int) -> None:
        self.add_or_remove(user_pk, self.following)

    def all_priv_rooms(self):
        return (priv_room(self, u2) for u2 in self.priv_chats.all())


def users():
    return User.objects

# class Message(models.Model):
#     author = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE
#     )
#
#     body = models.TextField()
#
#     room = models.ForeignKey(
#         PrivRoom,
#         on_delete=models.CASCADE
#     )
#
#     time_created = models.DateTimeField(
#         auto_now_add=True
#     )
#
