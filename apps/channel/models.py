from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Channel(models.Model):
    creator = models.ForeignKey(User, related_name='channels', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    main_channel = models.BooleanField(default=False)
    subject = models.CharField(max_length=100, blank=True, null=False)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=False)
    authors = models.ManyToManyField(User, related_name='author_channels', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'title:{self.title} id:{self.id}'
