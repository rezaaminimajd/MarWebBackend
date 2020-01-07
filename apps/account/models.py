from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=100)
    age = models.IntegerField()
    telephone_number = PhoneNumberField(null=False, blank=False, unique=True)

