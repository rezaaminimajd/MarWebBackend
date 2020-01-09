from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_polymorphic.serializers import PolymorphicSerializer

from apps.post import models as post_models


class PostAsListItemSerializer(ModelSerializer):
    pass


class PostSerializer(ModelSerializer):
    pass


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
