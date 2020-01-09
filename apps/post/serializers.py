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
        return post.profile.user.username

    class Meta:
        model = post_models.Post
        fields = ['type', 'title', 'post_owner', 'summary', 'media', 'create_date', 'update_date']


class PostSerializer(ModelSerializer):
    post_owner = SerializerMethodField('_post_owner')

    @staticmethod
    def _post_owner(post: post_models.Post):
        return post.profile.user.username

    class Meta:
        model = post_models.Post
        fields = ['type', 'title', 'post_owner', 'body', 'media', 'create_date', 'update_date']


class CommentSerializer(ModelSerializer):
    pass


class UserActionSerializer(ModelSerializer):
    pass


class UserActionPolymorphismSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        post_models.UserActionTemplate: UserActionSerializer,
        post_models.Post: PostSerializer,
        post_models.Comment: CommentSerializer,
    }
