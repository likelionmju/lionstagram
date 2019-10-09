from django.db import models
# 유저 정보 import
from django.conf import settings

class Profile(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='profile/', blank=True)

    def __str__(self):
        return self.name