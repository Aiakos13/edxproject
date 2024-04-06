from django.db import models
import datetime

# Create your models here.


class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
    