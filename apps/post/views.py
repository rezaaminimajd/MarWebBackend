from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.post.services.channel_posts_list import ChannelPosts
from . import models as post_models
from . import serializers as post_serializers


# Create your views here.


class ChannelPostsListAPIView(GenericAPIView):
    queryset = post_models.UserActionTemplate
    serializer_class = post_serializers.PostAsListItemSerializer

    def get(self, request, channel_id):
        posts, errors = ChannelPosts(channel_id=channel_id)()
        if errors:
            return Response(data={'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'posts': posts}, status=status.HTTP_200_OK)


class PostAPIView(GenericAPIView):

    def get(self, request, post_id):
        pass

    def post(self, request):
        pass

    def put(self, request, post_id):
        pass

    def delete(self, request, post_id):
        pass


class CommentsListAPIView(GenericAPIView):

    def get(self, request, post_id):
        pass


class CommentAPIView(GenericAPIView):

    def get(self, request, post_id, comment_id):
        pass

    def post(self, request, post_id):
        pass

    def put(self, request, post_id, comment_id):
        pass

    def delete(self, request, post_id, comment_id):
        pass


class LikeAPIView(GenericAPIView):

    def post(self, request, action_id):
        pass
