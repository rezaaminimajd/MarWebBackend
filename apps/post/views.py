from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import parsers

from apps.post.models import Post, Comment, UserActionTemplate, UserActionTypes, Like

from apps.post.serializers import PostSerializer, CommentSerializer
from apps.post.services.channel_posts_list import ChannelPosts
from apps.post.services.followed_channels_posts import FollowedChannelsPosts
from . import models as post_models
from . import serializers as post_serializers


# Create your views here.


class ChannelPostsListAPIView(GenericAPIView):
    queryset = post_models.UserActionTemplate
    serializer_class = post_serializers.PostAsListItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, channel_id):
        posts, errors = ChannelPosts(channel_id=channel_id)()
        if errors:
            return Response(data={'errors': errors}, status=status.HTTP_404_NOT_FOUND)
        data = self.get_serializer(posts, many=True).data
        return Response(data={'posts': data}, status=status.HTTP_200_OK)


class PostAPIView(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser,)

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        data = self.get_serializer(post).data
        return Response(data={'post': data}, status=status.HTTP_200_OK)

    def post(self, request):
        post = post_serializers.PostCreateSerializer(data=request.data)
        post.is_valid(raise_exception=True)
        post.save()
        return Response(data={'detail': 'Post has been submitted'}, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        user: User = request.user
        post: Post = get_object_or_404(Post, id=post_id)
        if user != post.user:
            return Response(data={'detail': 'this post is not for this user'}, status=status.HTTP_403_FORBIDDEN)
        target_post = self.get_serializer(data=request.data)
        target_post.is_valid(raise_exception=True)
        # todo nadombe
        return Response(data={'detail': 'post updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        user: User = request.user
        post: Post = get_object_or_404(Post, id=post_id)
        if user != post.user:
            return Response(data={'detail': 'this post is not for this user'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()  # todo nadombe
        return Response(data={'detail': 'post deleted successfully'}, status=status.HTTP_200_OK)


class CommentsListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post: Post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        return Response(data={'comments': comments}, status=status.HTTP_200_OK)


class CommentAPIView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, post=post, id=comment_id)
        data = self.get_serializer(comment).data
        return Response(data={'comment': data}, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        get_object_or_404(Post, id=post_id)
        comment = self.get_serializer(data=request.data)
        comment.is_valid(raise_exception=True)
        comment.save()
        return Response(data={'detail': 'comment has been submitted'}, status=status.HTTP_200_OK)

    def put(self, request, post_id, comment_id):
        user: User = request.user
        post = get_object_or_404(Post, id=post_id)
        comment = post.comments.filter(id=comment_id)
        if user != comment.user:
            return Response(data={'detail': 'this post is not for this user'}, status=status.HTTP_403_FORBIDDEN)

        # todo update

    def delete(self, request, post_id, comment_id):
        user: User = request.user
        post = get_object_or_404(Post, id=post_id)
        comment = post.comments.filter(id=comment_id)
        if user != comment.user:
            return Response(data={'detail': 'this post is not for this user'}, status=status.HTTP_403_FORBIDDEN)

        # todo delete


class LikeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action_id):
        action = get_object_or_404(UserActionTemplate, id=action_id)
        Like.objects.create(target=action, liker=request.user.profile)
        return Response(data={'detail': 'like successfully'}, status=status.HTTP_200_OK)


class NewPostsAPIVIew(GenericAPIView):
    queryset = UserActionTemplate.objects.all()
    serializer_class = post_serializers.PostAsListItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = self.get_queryset().filter(type=UserActionTypes.POST).order_by('-create_date')
        data = self.get_serializer(posts, many=True).data
        return Response(data={'posts': data}, status=status.HTTP_200_OK)


class HotPostsAPIView(GenericAPIView):
    queryset = UserActionTemplate.objects.all()
    serializer_class = post_serializers.PostAsListItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = self.get_queryset().filter(type=UserActionTypes.POST).annotate(likes_count=Count('likes')).order_by(
            '-likes_count')
        data = self.get_serializer(posts, many=True).data
        return Response(data={'posts': data}, status=status.HTTP_200_OK)


class FollowedChannelsPostsAPIView(GenericAPIView):
    serializer_class = post_serializers.PostAsListItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = FollowedChannelsPosts(request=request)()
        data = self.get_serializer(posts, many=True).data
        return Response(data={'posts': data}, status=status.HTTP_200_OK)


class ParticipatedPostsAPIView(GenericAPIView):
    serializer_class = post_serializers.PostAsListItemSerializer
    queryset = post_models.Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts_ids = self.get_queryset().filter(user=self.request.user).values_list('post_related_id', flat=True)
        posts = Post.objects.filter(id__in=posts_ids)
        data = self.get_serializer(posts, many=True).data
        return Response(data={'posts': data}, status=status.HTTP_200_OK)


class UserPostsListAPIView(GenericAPIView):
    serializer_class = post_serializers.PostAsListItemSerializer
    queryset = post_models.Post.objects.all()

    def get(self, request, username):
        data = self.get_serializer(self.get_queryset().filter(user__username=username), many=True).data
        return Response(data={'posts': data}, status=status.HTTP_200_OK)
