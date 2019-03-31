from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('publish')
    content = models.TextField()

    def __str__(self):
        return self.title
