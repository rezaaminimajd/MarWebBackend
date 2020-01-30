from django.shortcuts import render

from rest_framework.generics import GenericAPIView


from . import models as channel_models
from . import serializers as channel_serializers

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

    def get(self,request,searchQuery):
        channels = channel_models.Channel.objects.filter(name__startswith=searchQuery)
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
        pass

    def delete(self, request, channel_id):
        pass
