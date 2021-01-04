from django.db import models

# Create your models here.
from django.urls import reverse

from user.models import User


class Post(models.Model):

    content = models.TextField(
        null=False,
        blank=False,
        max_length=120
    )

    likes = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(likes__gte='0'),
                name='likes_non_negative'
            )
        ]

    def get_absolute_url(self):
        return reverse('view_post', args=[self.pk])

    def __str__(self):
        max_len = 10
        new_content = self.content[:max_len]
        if len(self.content) > len(new_content):
            new_content += '...'
        return f'{self.author}: "{new_content}" ({self.likes})'

