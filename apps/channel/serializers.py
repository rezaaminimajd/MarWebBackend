from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.channel import models as channel_models


class ChannelAsListItemSerializer(ModelSerializer):
    creator_username = SerializerMethodField('_creator_username')
    authors = SerializerMethodField('_authors')
    followers_count = SerializerMethodField('_followers_count')

    def _creator_username(self, channel: channel_models.Channel):
        return channel.creator.user.username

    def _authors(self, channel: channel_models.Channel):
        return ','.join(channel.authors.all().values_list('user__username', flat=True))

    def _followers_count(self, channel: channel_models.Channel):
        return channel.followers.count()

    class Meta:
        model = channel_models.Channel
        fields = ['name', 'creator_username', 'authors', 'followers_count', 'create_time']


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = channel_models.Channel
        fields = ['__all__']
