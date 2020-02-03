from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Channel(models.Model):
    creator = models.ForeignKey('account.Profile', related_name='channels', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    image = models.ImageField()
    authors = models.ManyToManyField(User, related_name='author_channels')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Topic(models.Model):
    channel = models.ForeignKey('channel.Channel', related_name='topics', on_delete=None, blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
