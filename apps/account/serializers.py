from rest_framework import serializers, status
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueValidator
from .models import *
from rest_polymorphic.serializers import PolymorphicSerializer


class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    user = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model: User
        fields = ['email', 'username', 'password', 'repeat_password']

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError('password don\'t match')
        return data


class ProfileSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Profile
        fields = ['__all__']


class FollowSerializers(serializers.ModelSerializer):
    source_name = SerializerMethodField('_source_name')

    @staticmethod
    def _source_name(follow: Follow):
        return follow.source.user.username

    class Meta:
        model = Follow
        fields = ['source_name']


class FollowUserSerializers(serializers.ModelSerializer):
    target_name = SerializerMethodField('_target_name')

    @staticmethod
    def _target_name(follow: FollowUser):
        return follow.target.user.username

    class Meta:
        model = FollowUser
        fields = ['target_name']


class FollowChannelSerializers(serializers.ModelSerializer):
    target_name = SerializerMethodField('_target_name')

    @staticmethod
    def _target_name(follow: FollowUser):
        return follow.target.user.username

    class Meta:
        model = FollowChannel
        fields = ['target_name']


class PolymorphicFollowSerializers(PolymorphicSerializer):
    follow_serializers = {
        Follow: FollowSerializers,
        FollowUser: FollowUserSerializers,
        FollowChannel: FollowChannelSerializers
    }
