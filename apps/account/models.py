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
    image = models.ImageField(null=True, blank=True)
    followers = models.ManyToManyField('self', related_name='followers')
    followings = models.ManyToManyField('self', related_name='followings')


class Follow(PolymorphicModel):
    source = models.ForeignKey('account.Profile', related_name='followings', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=FollowTypes.TYPES)


class FollowUser(Follow):
    target = models.ForeignKey('account.Profile', related_name='followers', on_delete=models.CASCADE)

    def pre_save(self):
        self.type = FollowTypes.USER

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)


class FollowChannel(Follow):
    target = models.ForeignKey('channel.Channel', related_name='followers', on_delete=models.CASCADE)

    def pre_save(self):
        self.type = FollowTypes.CHANNEL

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)
