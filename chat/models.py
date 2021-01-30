from django.db import models


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


# class LimitedModelMixin(models.Model):
#     limit: int
#
#     def save(self, *args, **kwargs):
#         if type(self).objects.count() >= type(self).limit:
#             type(self).objects[0].delete()
#
#         super().save()
#
#     class Meta:
#         abstract = True


class Message(models.Model):
    max_size = 100
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.TextField(blank=False, null=False)
    body = models.TextField(blank=False, null=False)

    def save(self, *args, **kwargs):
        if Message.objects.count() == Message.max_size:
            Message.objects[0].delete()

        super().save(*args, **kwargs)


def rooms():
    return Room.objects


def messages():
    return Message.objects
