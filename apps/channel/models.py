from django.db import models


# Create your models here.

class Channel(models.Model):
    from ..account.models import Profile
    creator = models.ForeignKey(Profile, related_name='channels', on_delete=models.CASCADE)
