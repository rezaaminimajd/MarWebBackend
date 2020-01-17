from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, timedelta

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
    image = models.ImageField(null=True, blank=True)


class Follow(PolymorphicModel):
    source = models.ForeignKey('account.Profile', related_name='followings', on_delete=models.CASCADE)
    follow_type = models.CharField(max_length=20, choices=FollowTypes.TYPES)


class FollowUser(Follow):
    target = models.ForeignKey('account.Profile', related_name='followers_user', on_delete=models.CASCADE)

    def pre_save(self):
        self.follow_type = FollowTypes.USER

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)


class FollowChannel(Follow):
    target = models.ForeignKey('channel.Channel', related_name='followers_channel', on_delete=models.CASCADE)

    def pre_save(self):
        self.follow_type = FollowTypes.CHANNEL

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)


class ProfileToken(models.Model):
    profile = models.ForeignKey(Profile, related_name='tokens', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def isValidToken(self):
        now = datetime.now()
        deadline = self.date + timedelta(hours=24)
        if now < deadline:
            return True
        return False
