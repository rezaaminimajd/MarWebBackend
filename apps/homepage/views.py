from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import documents
from ..post.serializers import PostAsListItemSerializer
from ..account.serializers import UserSerializerSecondType
from ..channel.serializers import ChannelAsListItemSerializer


# Create your views here.


class SearchAPIView(GenericAPIView):

    def get(self, request):
        q = request.GET.get('q', '')
        posts = documents.PostDocument.search().query("query_string", default_field='*',
                                                      query='*' + q + '*').to_queryset()
        channels = documents.ChannelDocument.search().query("query_string", default_field='*',
                                                            query='*' + q + '*').to_queryset()
        accounts = documents.UserDocument.search().query("query_string", default_field='*',
                                                         query='*' + q + '*').to_queryset()
        posts = PostAsListItemSerializer(posts, many=True).data
        channels = ChannelAsListItemSerializer(channels, many=True).data
        accounts = UserSerializerSecondType(accounts, many=True).data
        return Response(data={'posts': posts, 'channels': channels, 'accounts': accounts},
                        status=status.HTTP_200_OK)
