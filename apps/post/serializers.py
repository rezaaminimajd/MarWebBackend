from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_polymorphic.serializers import PolymorphicSerializer

from apps.post import models as post_models


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


class PostSerializer(ModelSerializer):
    post_owner = SerializerMethodField('_post_owner', read_only=True)

    @staticmethod
    def _post_owner(post: post_models.Post):
        return post.user.username

    class Meta:
        model = post_models.Post
        fields = ['id', 'title', 'post_owner', 'body', 'media', 'create_date', 'update_date']


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = post_models.Post
        fields = ['id', 'title', 'user', 'channel', 'body', 'media', 'create_date', 'update_date']


class SubCommentSerializer(ModelSerializer):
    comment_owner = SerializerMethodField()

    @staticmethod
    def _comment_owner(comment: post_models.Comment):
        return comment.user.username

    class Meta:
        model = post_models.Comment
        fields = ['id', 'post_related_id', 'title', 'comment_owner', 'body', 'media', 'create_date', 'update_date']


class CommentSerializer(ModelSerializer):
    parent_comment = PrimaryKeyRelatedField(read_only=True)
    replies = SubCommentSerializer(many=True)
    comment_owner = SerializerMethodField()

    @staticmethod
    def _comment_owner(comment: post_models.Comment):
        return comment.user.username

    class Meta:
        model = post_models.Comment
        fields = ['id', 'parent_comment', 'post_related_id', 'title', 'comment_owner', 'body', 'media', 'create_date',
                  'update_date', 'replies']


class UserActionPolymorphismSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        post_models.UserActionTemplate: UserActionSerializer,
        post_models.Post: PostSerializer,
        post_models.Comment: CommentSerializer,
    }
