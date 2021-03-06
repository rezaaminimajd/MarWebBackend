from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import parsers

from apps.post.models import Post, Comment, UserActionTemplate, UserActionTypes, Like, LikeTypes

from apps.post.serializers import PostSerializer, CommentSerializer, CommentCreateSerializer
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
        old_post = get_object_or_404(Post, id=post_id)
        if request.user.id != old_post.user.id:
            return Response(data={'errors': 'This Post doesnt belongs to you'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        new_post = post_serializers.PostCreateSerializer(instance=old_post, data=request.data)
        if new_post.is_valid(raise_exception=True):
            new_post.save()
            return Response(data={'detail': 'Post updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user.id != post.user.id:
            return Response(data={'errors': 'This Post doesnt belongs to you'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        post.delete()
        return Response(data={'detail': 'Your Post deleted Successfully'}, status=status.HTTP_200_OK)


class CommentsListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post: Post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        return Response(data={'comments': comments}, status=status.HTTP_200_OK)


class CommentAPIView(GenericAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request):
        comment = self.get_serializer(data=request.data)
        if comment.is_valid(raise_exception=True):
            comment.save()
            return Response(data={'detail': 'Comment has been submitted'}, status=status.HTTP_200_OK)
        return Response(data={'error': 'Comment not submitted! an error occurred'})

    def put(self, request, comment_id):
        old_comment = get_object_or_404(Comment, id=comment_id)
        if request.user.id != old_comment.user.id:
            return Response(data={'errors': 'This Comment doesnt belongs to you'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        new_comment = self.get_serializer(instance=old_comment, data=request.data)
        if new_comment.is_valid(raise_exception=True):
            new_comment.save()
            return Response(data={'detail': 'Comment updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user.id != comment.user.id:
            return Response(data={'errors': 'This Comment doesnt belongs to you'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        comment.delete()
        return Response(data={'detail': 'Your Comment deleted Successfully'}, status=status.HTTP_200_OK)


class LikeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action_id):
        action = get_object_or_404(UserActionTemplate, id=action_id)
        if Like.objects.filter(target=action, liker=request.user, type=LikeTypes.LIKE).exists():
            return Response(data={'detail': 'Action already liked'}, status=status.HTTP_200_OK)
        try:
            Like.objects.get(target=action, liker=request.user, type=LikeTypes.DISLIKE).delete()
        except Like.DoesNotExist:
            pass
        Like.objects.create(target=action, liker=request.user, type=LikeTypes.LIKE)
        return Response(data={'detail': 'Liked successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, action_id):
        action = get_object_or_404(UserActionTemplate, id=action_id)
        try:
            Like.objects.get(target=action, liker=request.user, type=LikeTypes.LIKE).delete()
            return Response(data={'detail': 'Action unliked'})
        except Like.DoesNotExist:
            return Response(data={'detail': 'Action already unliked'})


class DisLikeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action_id):
        action = get_object_or_404(UserActionTemplate, id=action_id)
        if Like.objects.filter(target=action, liker=request.user, type=LikeTypes.DISLIKE).exists():
            return Response(data={'detail': 'Action already disliked'}, status=status.HTTP_200_OK)
        try:
            Like.objects.get(target=action, liker=request.user, type=LikeTypes.LIKE).delete()
        except Like.DoesNotExist:
            pass
        Like.objects.create(target=action, liker=request.user, type=LikeTypes.DISLIKE)
        return Response(data={'detail': 'Disliked successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, action_id):
        action = get_object_or_404(UserActionTemplate, id=action_id)
        try:
            Like.objects.get(target=action, liker=request.user, type=LikeTypes.DISLIKE).delete()
            return Response(data={'detail': 'Action disliked'})
        except Like.DoesNotExist:
            return Response(data={'detail': 'Action already disliked'})


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
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        data = self.get_serializer(self.get_queryset().filter(user__username=username), many=True).data
        return Response(data={'posts': data}, status=status.HTTP_200_OK)
