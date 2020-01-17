from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.channel import models as channel_models
from apps.post.serializers import PostAsListItemSerializer


class TopicSerializer(ModelSerializer):
    class Meta:
        model = channel_models.Topic
        fields = ['name']


class ChannelAsListItemSerializer(ModelSerializer):
    creator_username = SerializerMethodField('_creator_username')
    authors = SerializerMethodField('_authors')
    followers_count = SerializerMethodField('_followers_count')
    topics = TopicSerializer(many=True, read_only=True)

    @staticmethod
    def _creator_username(channel: channel_models.Channel):
        return channel.creator.user.username

    @staticmethod
    def _authors(channel: channel_models.Channel):
        return ','.join(channel.authors.all().values_list('user__username', flat=True))

    @staticmethod
    def _followers_count(channel: channel_models.Channel):
        return channel.followers_channel.count()

    class Meta:
        model = channel_models.Channel
        fields = ['name', 'topics', 'creator_username', 'authors', 'followers_count', 'create_time']


class ChannelSerializer(ModelSerializer):
    posts = PostAsListItemSerializer(many=True, read_only=True)
    creator_username = SerializerMethodField('_creator_username')
    authors = SerializerMethodField('_authors')
    followers_count = SerializerMethodField('_followers_count')
    topics = TopicSerializer(many=True, read_only=True)

    @staticmethod
    def _creator_username(channel: channel_models.Channel):
        return channel.creator.user.username

    @staticmethod
    def _authors(channel: channel_models.Channel):
        return ','.join(channel.authors.all().values_list('user__username', flat=True))

    @staticmethod
    def _followers_count(channel: channel_models.Channel):
        return channel.followers_channel.count()

    class Meta:
        model = channel_models.Channel
        fields = ['name', 'topics', 'creator_username', 'authors', 'followers_count', 'create_time', 'update_time',
                  'posts']
