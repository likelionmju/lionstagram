from django.conf import settings
from django.db import models
# 유저 정보 import


class Profile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='profile/', blank=True)
