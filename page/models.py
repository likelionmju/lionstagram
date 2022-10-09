from django.conf import settings
from django.db import models
# 유저 정보 import

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='likes',
        through='Like',
    )
    pub_date = models.DateTimeField('publish')
    image = models.ImageField(upload_to='images/', blank=True)
    content = models.TextField()

    def __str__(self):
        return self.content[:20]

    def summary(self):
        return self.content[:100]

    # Count Total_Likes
    def likes_count(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
