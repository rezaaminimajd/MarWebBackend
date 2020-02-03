from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status

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

    def get(self, request, channel_id):
        pass

    def post(self, request):
        pass

    def put(self, request, channel_id):
        pass

    def delete(self, request, channel_id):
        pass


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
