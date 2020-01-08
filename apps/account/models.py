from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    age = models.IntegerField()
    telephone_number = PhoneNumberField(unique=True)


class Follow(models.Model):
    source = models.ForeignKey(Profile, related_name='follows', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class FollowUser(Follow):
    target = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)


class FollowChannel(Follow):
    from ..channel.models import Channel
    target = models.ForeignKey(Channel, related_name='followers', on_delete=models.CASCADE)
