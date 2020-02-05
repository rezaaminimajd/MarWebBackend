from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from rest_framework import serializers

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

    def update(self, instance: channel_models.Channel, validated_data):
        instance.creator = validated_data.get('creator', instance.creator)
        instance.title = validated_data.get('title', instance.title)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.image = validated_data.get('image', instance.image)
        instance.authors.add(validated_data.get('authors', instance.authors))
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ChanelUpdateSerializer(ModelSerializer):
    class Meta:
        model = channel_models.Channel
        fields = ['creator', 'title', 'subject', 'image', 'authors', 'description']
