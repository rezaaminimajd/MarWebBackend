from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from apps.post.services.channel_posts_list import ChannelPosts
from . import models as post_models
from . import serializers as post_serializers


# Create your views here.


class ChannelPostsListAPIView(GenericAPIView):
    serializer_class = post_serializers.PostAsListItemSerializer

    def get(self, request, channel_id):
        posts, errors = ChannelPosts(channel_id=channel_id)()
        if errors:
            return Response(data={'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        data = self.get_serializer(posts, many=True, read_only=True)
        return Response(data={'posts': data}, status=status.HTTP_200_OK)


class PostDetailAPIView(GenericAPIView):
    queryset = post_models.Post.objects.all()
    serializer_class = post_serializers.PostSerializer

    def get(self, request, post_id):
        post = get_object_or_404(post_models.Post, id=post_id)
        data = self.get_serializer(post, read_only=True).data
        return Response(data={'post': data}, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        pass

    def delete(self, request, post_id):
        post_models.Post.objects.filter(id=post_id).delete()


class NewPostAPIView(GenericAPIView):
    serializer_class = post_serializers.PostSerializer

    def post(self, request, channel_id):
        channel = get_object_or_404()


class CommentsListAPIView(GenericAPIView):
    serializer_class = post_serializers.CommentSerializer
    queryset = post_models.Comment.objects.all()

    def get(self, request, post_id):
        if not post_models.Post.objects.filter(id=post_id).exists():
            return Response(data={'errors': ['Post with given id not exists']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        comments = self.get_queryset().filter(post_related_id=post_id)
        data = self.get_serializer(comments, many=True).data
        return Response(data={'comments': data}, status=status.HTTP_200_OK)


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
