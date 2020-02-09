from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from ..post import models as post_models
from ..channel import models as channel_models
from ..account import models as account_models
from .models import Notification, NotificationTypes


@receiver(post_save, sender=post_models.Post)
def new_post(sender, instance: post_models.Post, created, **kwargs):
    if created:
        followers_ids = instance.channel.followers_channel.all().values_list('source', flat=True)
        followers = User.objects.filter(id__in=followers_ids)
        notifications = [Notification(from_user=instance.user,
                                      to_user=follower,
                                      target_id=instance.id,
                                      type=NotificationTypes.POST) for follower in followers]
        objs = Notification.objects.bulk_create(notifications)


@receiver(post_save, sender=post_models.Comment)
def new_comment(sender, instance: post_models.Comment, created, **kwargs):
    if created:
        post_owner = instance.post_related.user
        Notification.objects.create(from_user=instance.user, to_user=post_owner, target_id=instance.post_related.id,
                                    type=NotificationTypes.COMMENT)
        if instance.parent_comment:
            Notification.objects.create(from_user=instance.user, to_user=instance.parent_comment.user,
                                        target_id=instance.post_related.id)


@receiver(post_save, sender=post_models.Like)
def like(sender, instance: post_models.Like, created, **kwargs):
    if created:
        action_owner = instance.target.user
        Notification.objects.create(from_user=instance.liker, to_user=action_owner, target_id=instance.target_id,
                                    type=NotificationTypes.LIKE)


@receiver(post_save, sender=account_models.FollowUser)
def follow_user(sender, instance: account_models.FollowUser, created, **kwargs):
    if created:
        followed_user = instance.target
        Notification.objects.create(from_user=instance.source, to_user=followed_user, target_id=instance.target.id,
                                    type=NotificationTypes.FOLLOW_USER)


@receiver(post_save, sender=account_models.FollowChannel)
def follow_channel(sender, instance: account_models.FollowChannel, created, **kwargs):
    if created and not instance.target.main_channel:
        followed_channel_owner = instance.target.creator
        notif = Notification.objects.create(from_user=instance.source, to_user=followed_channel_owner,
                                            target_id=instance.target.id, type=NotificationTypes.FOLLOW_CHANNEL)
