from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_polymorphic.serializers import PolymorphicSerializer

from apps.account.serializers import UserSerializers, UserSerializerSecondType
from apps.post import models as post_models
from apps.post.models import LikeTypes


class PostAsListItemSerializer(ModelSerializer):
    summary = SerializerMethodField('_summary')
    post_owner = SerializerMethodField('_post_owner')

    @staticmethod
    def _summary(post: post_models.Post):
        return post.post_summary

    @staticmethod
    def _post_owner(post: post_models.Post):
        return post.user.username

    class Meta:
        model = post_models.Post
        fields = ['id', 'type', 'title', 'post_owner', 'summary', 'media', 'create_date', 'update_date']


class UserActionSerializer(ModelSerializer):
    owner = SerializerMethodField('_owner')

    @staticmethod
    def _owner(action: post_models.UserActionTemplate):
        return action.user.username

    class Meta:
        model = post_models.UserActionTemplate
        fields = ['id', 'type', 'owner', 'body', 'media', 'create_date', 'update_date']


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = post_models.Post
        fields = ['title', 'user', 'channel', 'body', 'media']


class SubCommentSerializer(ModelSerializer):
    user = UserSerializerSecondType(read_only=True)
    likes = serializers.SerializerMethodField('_likes')
    dislikes = serializers.SerializerMethodField('_dislikes')

    @staticmethod
    def _likes(post: post_models.Post):
        return post.likes.filter(type=LikeTypes.LIKE).count()

    @staticmethod
    def _dislikes(post: post_models.Post):
        return post.likes.filter(type=LikeTypes.DISLIKE).count()

    class Meta:
        model = post_models.Comment
        fields = ['id', 'likes', 'dislikes', 'post_related', 'user', 'body', 'media', 'create_date', 'update_date']


class CommentSerializer(ModelSerializer):
    parent_comment = PrimaryKeyRelatedField(read_only=True)
    replies = SubCommentSerializer(many=True)
    user = UserSerializerSecondType(read_only=True)
    likes = serializers.SerializerMethodField('_likes')
    dislikes = serializers.SerializerMethodField('_dislikes')

    @staticmethod
    def _likes(post: post_models.Post):
        return post.likes.filter(type=LikeTypes.LIKE).count()

    @staticmethod
    def _dislikes(post: post_models.Post):
        return post.likes.filter(type=LikeTypes.DISLIKE).count()

    class Meta:
        model = post_models.Comment
        fields = ['id', 'likes', 'dislikes', 'parent_comment', 'post_related', 'user', 'body', 'media',
                  'create_date',
                  'update_date', 'replies']


class PostSerializer(ModelSerializer):
    user = UserSerializerSecondType(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = serializers.SerializerMethodField('_likes')
    dislikes = serializers.SerializerMethodField('_dislikes')

    @staticmethod
    def _likes(post: post_models.Post):
        return post.likes.filter(type=LikeTypes.LIKE).count()

    @staticmethod
    def _dislikes(post: post_models.Post):
        return post.likes.filter(type=LikeTypes.DISLIKE).count()

    class Meta:
        model = post_models.Post
        fields = ['id', 'likes', 'dislikes', 'title', 'user', 'channel', 'body', 'media', 'likes', 'create_date',
                  'update_date', 'comments']


class UserActionPolymorphismSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        post_models.UserActionTemplate: UserActionSerializer,
        post_models.Post: PostSerializer,
        post_models.Comment: CommentSerializer,
    }
