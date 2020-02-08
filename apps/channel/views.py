from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import status
from rest_framework import parsers, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.account.models import FollowTypes
from apps.channel.models import Channel
from . import models as channel_models
from . import serializers as channel_serializers
from apps.account import models as account_models


# Create your views here.

class TopChannelsAPIView(GenericAPIView):
    queryset = channel_models.Channel.objects.all()
    serializer_class = channel_serializers.ChannelAsListItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        channels = self.get_queryset().annotate(followers_count=Count('followers_channel')).order_by('-followers_count')
        data = self.get_serializer(channels, many=True).data
        return Response(data={'channels': data}, status=status.HTTP_200_OK)


class UserChannelsListAPIView(GenericAPIView):
    queryset = channel_models.Channel.objects.all()
    serializer_class = channel_serializers.ChannelAsListItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        channels = self.get_queryset().filter(creator__username=username)
        data = self.get_serializer(channels, many=True).data
        return Response(data={'channels': data}, status=status.HTTP_200_OK)


class ChannelAPIView(GenericAPIView):
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, channel_id):
        channel = get_object_or_404(channel_models.Channel, id=channel_id)
        data = channel_serializers.ChannelSerializer(channel).data
        return Response(data={'channel': data})

    def post(self, request):
        new_channel = channel_serializers.ChannelPostSerializer(data=request.data)
        if new_channel.is_valid(raise_exception=True):
            new_channel = new_channel.save()
            return Response(data={'detail': channel_serializers.ChannelSerializer(new_channel).data},
                            status=status.HTTP_200_OK)
        return Response(data={'errors': 'Error occurred, channel not created!'})

    def put(self, request, channel_id):
        channel = get_object_or_404(Channel, id=channel_id)
        updated_channel = channel_serializers.ChannelPostSerializer(instance=channel, data=request.data)
        if updated_channel.is_valid(raise_exception=True):
            updated_channel.save()
            return Response(data={'detail': 'Channel updated successfully'})
        return Response(data={'error': 'Channel not updated ! An error occurred'})

    def delete(self, request, channel_id):
        channel = get_object_or_404(channel_models.Channel, id=channel_id)
        channel.delete()
        return Response(data={'detail': 'Channel deleted successfully'}, status=status.HTTP_200_OK)


class FollowAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, channel_id):
        source: User = request.user
        target: Channel = get_object_or_404(channel_models.Channel, id=channel_id)
        if account_models.FollowChannel.objects.filter(source=source, target=target).exists():
            return Response(data={'detail': 'Already followed'}, status=status.HTTP_200_OK)
        account_models.FollowChannel.objects.create(source=source, target=target)
        return Response(data={'detail': 'followed successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, channel_id):
        deleted, _ = account_models.FollowChannel.objects.filter(source=request.user, target__id=channel_id).delete()
        if deleted:
            return Response(data={'detail': 'You Successfully unFollowed this channel'}, status=status.HTTP_200_OK)
        return Response(data={'errors': 'Unexpected error occurred'}, status=status.HTTP_200_OK)
