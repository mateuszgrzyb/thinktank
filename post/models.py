from django.db import models

# Create your models here.
from django.urls import reverse


class Post(models.Model):
    content = models.TextField(
        null=False,
        blank=False,
        max_length=120
    )

    likes = models.ManyToManyField(
        to='user.User',
        blank=True,
        related_name='posts_liked_by_user'
    )

    author = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse('view_post', args=[self.pk])

    def __str__(self):
        max_len = 10
        new_content = self.content[:max_len]
        if len(self.content) > len(new_content):
            new_content += '...'
        return f'{self.author}: "{new_content}" ({self.likes.count()})'


def posts():
    return Post.objects
