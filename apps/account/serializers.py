from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import *


class UserSerializers(serializers.ModelSerializer):
    pass


class ProfileSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Profile
        fields = ['__all__']


class FollowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = []


class FollowUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = FollowUser
        fields = ['target']


class FollowChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model = FollowChannel
        fields = ['target']


class PolymorphicFollowSerializers(serializers.ModelSerializer):
    pass
