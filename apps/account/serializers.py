from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueValidator
from rest_polymorphic.serializers import PolymorphicSerializer

from apps.channel.models import Channel
from .models import *


class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    repeat_password = serializers.CharField(max_length=100, required=False)
    age = serializers.IntegerField(required=False)
    telephone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'repeat_password', 'age', 'telephone_number', 'first_name',
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
        channel = Channel.objects.create(creator=user, title=user.username, main_channel=True)
        channel.authors.add(user)
        return user

    def validate(self, data):
        if 'repeat_password' not in data.keys() or data['password'] != data['repeat_password']:
            raise serializers.ValidationError('password don\'t match')
        return data


class ProfileSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Profile
        fields = ['age', 'telephone_number', 'user', 'image']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    age = serializers.IntegerField()
    telephone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    image = serializers.ImageField()

    class Meta:
        model = User
        fields = ['id', 'email', 'age', 'telephone_number', 'first_name', 'last_name', 'image']

    def update(self, instance: User, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile.age = validated_data.get('age', instance.profile.age)
        instance.profile.telephone_number = validated_data.get('telephone_number', instance.profile.telephone_number)
        instance.profile.image = validated_data.get('image', instance.profile.image)
        instance.save()
        instance.profile.save()
        return instance


class FollowSerializers(serializers.ModelSerializer):
    source_name = SerializerMethodField('_source_name')

    @staticmethod
    def _source_name(follow: Follow):
        return follow.source.username

    class Meta:
        model = Follow
        fields = ['source_name']


class FollowUserSerializers(serializers.ModelSerializer):
    target_name = SerializerMethodField('_target_name')
    source_name = SerializerMethodField('_source_name')

    @staticmethod
    def _source_name(follow: FollowUser):
        return follow.source.username

    @staticmethod
    def _target_name(follow: FollowUser):
        return follow.target.username

    class Meta:
        model = FollowUser
        fields = ['target_name', 'source_name']


class FollowChannelSerializers(serializers.ModelSerializer):
    target_name = SerializerMethodField('_target_name')
    source_name = SerializerMethodField('_source_name')

    @staticmethod
    def _source_name(follow: FollowChannel):
        return follow.source.username

    @staticmethod
    def _target_name(follow: FollowChannel):
        return follow.target.title

    class Meta:
        model = FollowChannel
        fields = ['target_name', 'source_name']


class PolymorphicFollowSerializers(PolymorphicSerializer):
    model_serializer_mapping = {
        Follow: FollowSerializers,
        FollowUser: FollowUserSerializers,
        FollowChannel: FollowChannelSerializers,
    }


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ForgotPasswordConfirmSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(max_length=100)
    new_password2 = serializers.CharField(max_length=100)

    class Meta:
        model = ForgotPasswordToken
        fields = ['new_password1', 'new_password2', 'uid', 'token']

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('passwords don\'t match!')
        return data
