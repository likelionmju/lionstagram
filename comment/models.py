from django.conf import settings
from django.db import models

from page.models import Post
# 유저 정보 import

# Create your models here.


class Comment(models.Model):
    # related_name
    title = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField('publish')
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content
