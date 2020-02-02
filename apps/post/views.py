from django.contrib.auth.models import User
from django.core.serializers import get_serializer
from django.shortcuts import render, get_object_or_404
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.post.models import Post, Comment
from apps.post.serializers import PostSerializer, CommentSerializer
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
    serializer_class = PostSerializer

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        return Response(data={'post': post}, status=status.HTTP_200_OK)

    def post(self, request):
        post = self.get_serializer(data=request.data)
        post.is_valid(raise_exception=True)
        post.save()
        return Response(data={'detail': 'post has been registered'}, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        user: User = request.user
        post: Post = get_object_or_404(Post, id=post_id)
        if user != post.profile.user:
            return Response(data={'detail': 'this post is not for this user'}, status=status.HTTP_403_FORBIDDEN)
        target_post = self.get_serializer(data=request.data)
        target_post.is_valid(raise_exception=True)
        # todo nadombe
        return Response(data={'detail': 'post updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        user: User = request.user
        post: Post = get_object_or_404(Post, id=post_id)
        if user != post.profile.user:
            return Response(data={'detail': 'this post is not for this user'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()  # todo nadombe
        return Response(data={'detail': 'post deleted successfully'}, status=status.HTTP_200_OK)


class CommentsListAPIView(GenericAPIView):

    def get(self, request, post_id):
        post: Post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        return Response(data={'comments': comments}, status=status.HTTP_200_OK)


class CommentAPIView(GenericAPIView):
    serializer_class = CommentSerializer

    def get(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = post.comments.filter(id=comment_id)
        # if comment not exist response error
        return Response(data={'comment': comment}, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        get_object_or_404(Post, id=post_id)
        comment = self.get_serializer(data=request.data)
        comment.is_valid(raise_exception=True)
        comment.save()
        return Response(data={'detail': 'comment has been registered'}, status=status.HTTP_200_OK)

    def put(self, request, post_id, comment_id):
        user: User = request.user
        post = get_object_or_404(Post, id=post_id)
        comment = post.comments.filter(id=comment_id)
        if user != comment.profile.user:
            return Response(data={'detail': 'this post is not for this user'}, status=status.HTTP_403_FORBIDDEN)

        # todo update

    def delete(self, request, post_id, comment_id):
        user: User = request.user
        post = get_object_or_404(Post, id=post_id)
        comment = post.comments.filter(id=comment_id)
        if user != comment.profile.user:
            return Response(data={'detail': 'this post is not for this user'}, status=status.HTTP_403_FORBIDDEN)

        # todo delete


class LikeAPIView(GenericAPIView):

    def post(self, request, action_id):
        pass


class NewPostsAPIVIew(GenericAPIView):
    pass


class HotPostsAPIView(GenericAPIView):
    queryset = Post.objects.all()

    def get(self):
        pass  # todo bazen bazen bega hade


