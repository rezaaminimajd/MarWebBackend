from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from polymorphic.models import PolymorphicModel


class FollowTypes:
    CHANNEL = 'channel'
    USER = 'user'
    TYPES = (
        (CHANNEL, 'Channel Follow'),
        (USER, 'User Follow')
    )


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    age = models.IntegerField()
    telephone_number = PhoneNumberField(unique=True)


class Follow(PolymorphicModel):
    source = models.ForeignKey(Profile, related_name='followings', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=FollowTypes.TYPES)


class FollowUser(Follow):
    target = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)

    def pre_save(self):
        self.type = FollowTypes.USER

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)


class FollowChannel(Follow):
    from ..channel.models import Channel
    target = models.ForeignKey(Channel, related_name='followers', on_delete=models.CASCADE)

    def pre_save(self):
        self.type = FollowTypes.CHANNEL

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)
