from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.account.models import FollowTypes
from apps.channel.models import Channel
from . import models as channel_models
from . import serializers as channel_serializers
from apps.account import models as account_models


# Create your views here.


class ChannelsListAPIView(GenericAPIView):
    queryset = channel_models.Channel.objects.all()
    serializer_class = channel_serializers.ChannelAsListItemSerializer

    def get(self, request):
        channels = channel_models.Channel.objects.all()
        data = self.get_serializer(channels, many=True, read_only=True).data
        print('data:', data)
        return Response(data={'channels': data}, status=status.HTTP_200_OK)


class ChannelsSearchListAPIView(GenericAPIView):
    queryset = channel_models.Channel.objects.all()
    serializer_class = channel_serializers.ChannelAsListItemSerializer

    def get(self, request, search_query):
        channels = channel_models.Channel.objects.filter(name__startswith=search_query)
        data = self.get_serializer(channels, many=True).data
        print('data:', data)
        return Response(data={'channels': data}, status=status.HTTP_200_OK)


class ChannelAPIView(GenericAPIView):
    parser_classes = (parsers.MultiPartParser,)

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

    def put(self, request, channel_id):
        get_object_or_404(channel_models.Channel, id=channel_id)
        # TODO complete this APIView

    def delete(self, request, channel_id):
        channel = get_object_or_404(channel_models.Channel, id=channel_id)
        channel.delete()
        return Response(data={'detail': 'Channel deleted successfully'}, status=status.HTTP_200_OK)


class FollowAPIView(GenericAPIView):

    def post(self, request, channel_id):
        source: User = request.user
        target: Channel = get_object_or_404(channel_models.Channel, id=channel_id)
        follow_model = account_models.Follow.objects.create(source=source.profile, target=target,
                                                            follow_type=FollowTypes.CHANNEL)
        follow_model.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, channel_id):
        source: User = request.user
        target: Channel = get_object_or_404(channel_models.Channel, id=channel_id)
        account_models.FollowChannel.objects.filter(source=source.profile).filter(target=target).delete()
        return Response(status=status.HTTP_200_OK)
