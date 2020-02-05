from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from apps.account.serializers import UserSerializers, PolymorphicFollowSerializers
from apps.channel import models as channel_models
from apps.post.serializers import PostAsListItemSerializer


class ChannelAsListItemSerializer(ModelSerializer):
    creator_username = SerializerMethodField('_creator_username')
    authors = UserSerializers(many=True, read_only=True)
    followers_count = SerializerMethodField('_followers_count')

    @staticmethod
    def _creator_username(channel: channel_models.Channel):
        return channel.creator.username

    @staticmethod
    def _followers_count(channel: channel_models.Channel):
        return channel.followers_channel.count()

    class Meta:
        model = channel_models.Channel
        fields = ['id', 'title', 'subject', 'creator_username', 'main_channel', 'image', 'description', 'authors',
                  'followers_count', 'create_time', 'update_time']


class ChannelSerializer(ModelSerializer):
    posts = PostAsListItemSerializer(many=True, read_only=True)
    creator_username = SerializerMethodField('_creator_username')
    authors = UserSerializers(many=True, read_only=True)
    followers_count = SerializerMethodField('_followers_count')
    followers_channel = PolymorphicFollowSerializers(read_only=True, many=True)

    @staticmethod
    def _creator_username(channel: channel_models.Channel):
        return channel.creator.username

    @staticmethod
    def _followers_count(channel: channel_models.Channel):
        return channel.followers_channel.count()

    class Meta:
        model = channel_models.Channel
        fields = ['id', 'title', 'subject', 'description', 'creator_username', 'authors', 'followers_count',
                  'create_time',
                  'update_time',
                  'posts', 'image', 'followers_channel']


class ChannelPostSerializer(ModelSerializer):
    class Meta:
        model = channel_models.Channel
        fields = ['creator', 'title', 'subject', 'image', 'authors', 'description']
