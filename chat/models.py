from django.db import models


class Room(models.Model):
    url = models.TextField(blank=False, null=False)
    name = models.TextField(blank=False, null=False)
    anonymous = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id', 'anonymous'],
                name='composite primary key',
            )
        ]

    def __str__(self):
        return f'{self.name}'


def rooms():
    return Room.objects
