from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.channel import models as channel_models


class ChannelAsListItemSerializer(ModelSerializer):
    creator_username = SerializerMethodField('_creator_username')
    authors = SerializerMethodField('_authors')
    followers_count = SerializerMethodField('_followers_count')

    @staticmethod
    def _creator_username(channel: channel_models.Channel):
        return channel.creator.user.username

    @staticmethod
    def _authors(channel: channel_models.Channel):
        return ','.join(channel.authors.all().values_list('user__username', flat=True))

    @staticmethod
    def _followers_count(channel: channel_models.Channel):
        return channel.followers.count()

    class Meta:
        model = channel_models.Channel
        fields = ['name', 'creator_username', 'authors', 'followers_count', 'create_time']


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = channel_models.Channel
        fields = ['__all__']
