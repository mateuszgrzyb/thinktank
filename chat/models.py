import uuid

from django.db import models

from user.models import User


class Room(models.Model):
    anonymous = models.BooleanField(default=False)
    name = models.TextField(blank=False, null=False)
    url = models.TextField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['url', 'anonymous'],
                name='composite primary key',
            )
        ]

    def __str__(self):
        return f'{self.name}'


def rooms():
    return Room.objects


