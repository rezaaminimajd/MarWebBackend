from django.shortcuts import render

from rest_framework.generics import GenericAPIView

from . import serializers as channel_serializers


# Create your views here.


class ChannelsListAPIView(GenericAPIView):

    def get(self, request):
        pass


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
        pass

    def delete(self, request, channel_id):
        pass
