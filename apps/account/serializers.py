from rest_framework import serializers, status
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueValidator
from .models import *
from rest_polymorphic.serializers import PolymorphicSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.hashers import make_password


class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    repeat_password = serializers.CharField(max_length=100, required=False)
    age = serializers.IntegerField(required=False)
    telephone_number = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'repeat_password', 'age', 'telephone_number', 'first_name',
                  'last_name']

    def create(self, validated_data):
        if 'repeat_password' not in validated_data.keys() or 'telephone_number' not in validated_data.keys():
            raise serializers.ValidationError('age and telephone_number field is required')
        age = validated_data.pop('age')
        validated_data.pop('repeat_password')
        password = validated_data['password']
        validated_data['password'] = make_password(password)
        telephone_number = validated_data.pop('telephone_number')
        user = User.objects.create(**validated_data)
        profile = Profile.objects.create(user=user, age=age, telephone_number=telephone_number)
        ProfileToken.objects.create(profile=profile, date=datetime.now())
        return user

    def validate(self, data):
        if 'repeat_password' not in data.keys() or data['password'] != data['repeat_password']:
            raise serializers.ValidationError('password don\'t match')
        return data


class ProfileSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Profile
        fields = ['age', 'telephone_number', 'user']


class FollowSerializers(serializers.ModelSerializer):
    source_name = SerializerMethodField('_source_name')

    @staticmethod
    def _source_name(follow: Follow):
        return follow.source.user.username

    class Meta:
        model = Follow
        fields = ['source_name']


class FollowUserSerializers(serializers.ModelSerializer):
    target_name = SerializerMethodField('_target_name')
    source_name = SerializerMethodField('_source_name')

    @staticmethod
    def _source_name(follow: Follow):
        return follow.source.user.username

    @staticmethod
    def _target_name(follow: FollowUser):
        return follow.target.user.username

    class Meta:
        model = FollowUser
        fields = ['target_name', 'source_name']


class FollowChannelSerializers(serializers.ModelSerializer):
    target_name = SerializerMethodField('_target_name')
    source_name = SerializerMethodField('_source_name')


    @staticmethod
    def _source_name(follow: Follow):
        return follow.source.user.username

    @staticmethod
    def _target_name(follow: FollowUser):
        return follow.target.user.username

    class Meta:
        model = FollowChannel
        fields = ['target_name', 'source_name']


class PolymorphicFollowSerializers(PolymorphicSerializer):
    model_serializer_mapping = {
        Follow: FollowSerializers,
        FollowUser: FollowUserSerializers,
        FollowChannel: FollowChannelSerializers,
    }
