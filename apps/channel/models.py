from django.db import models


# Create your models here.

class Channel(models.Model):
    from ..account.models import Profile
    creator = models.ForeignKey(Profile, related_name='channels', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Profile, related_name='author_channels')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

