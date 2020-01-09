from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    age = models.IntegerField()
    telephone_number = PhoneNumberField(unique=True)
    image = models.ImageField(null=True, blank=True)
    followers = models.ManyToManyField('self', related_name='followers')
    followings = models.ManyToManyField('self', related_name='followings')



