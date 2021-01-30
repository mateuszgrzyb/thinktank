import uuid
from typing import Type

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    def add_or_remove(self, pk: int, group) -> None:
        if group.filter(pk=pk).exists():
            group.remove(pk)
        else:
            group.add(pk)

    def click_like(self, post_pk: int) -> None:
        self.add_or_remove(post_pk, self.posts_liked_by_user)

    def click_follow(self, user_pk: int) -> None:
        self.add_or_remove(user_pk, self.following)

    def get_all_priv_rooms(self):
        return PrivRoom.objects.filter(Q(user1=self) | Q(user2=self))


def users():
    return User.objects


class PrivRoom(models.Model):
    user1 = models.ForeignKey(
        User,
        related_name='user1',
        on_delete=models.CASCADE,
    )

    user2 = models.ForeignKey(
        User,
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

    @classmethod
    def create(cls, user1, user2):
        if user1 != user2 and priv_room(user1, user2) is not None:
            cls.objects.create(user1=user1, user2=user2)


def priv_rooms():
    return PrivRoom.objects.all()


def priv_room(u1, u2):
    rooms = priv_rooms().filter(
        (Q(user1=u1) & Q(user2=u2)) |
        (Q(user1=u2) & Q(user2=u1))
    )
    print(f'rooms found: {rooms.count()}')
    return rooms.first()


