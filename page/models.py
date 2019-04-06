from django.db import models
# 유저 정보 import
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('publish')
    image = models.ImageField(upload_to='images/', blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:100]
