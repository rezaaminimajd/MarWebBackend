from django.contrib.auth.models import User
from django.db import models


class NotificationTypes:
    FOLLOW_USER = 'follow_user'
    FOLLOW_CHANNEL = 'follow_channel'
    LIKE = 'like'
    POST = 'post'
    COMMENT = 'comment'
    TYPES = (
        (FOLLOW_USER, 'follow user'),
        (FOLLOW_CHANNEL, 'follow channel'),
        (LIKE, 'like'),
        (POST, 'new post'),
        (COMMENT, 'new comment'),
    )


class Notification(models.Model):
    """
        target_id: should be the id of user that followed or post or comment that
            liked or post that commented
    """
    from_user = models.ForeignKey(User, related_name='sent_notifications', on_delete=None)
    to_user = models.ForeignKey(User, related_name='received_notifications', on_delete=None)
    message = models.CharField(max_length=200, null=True, blank=True)
    target_id = models.IntegerField()
    type = models.CharField(choices=NotificationTypes.TYPES, max_length=20)
    seen = models.BooleanField(default=False)

    def pre_save(self):
        if self.type == NotificationTypes.FOLLOW_USER:
            self.message = f'{self.from_user.username} followed you.'
        elif self.type == NotificationTypes.FOLLOW_CHANNEL:
            self.message = f'{self.from_user.username} followed your channel with id {self.target_id}'
        elif self.type == NotificationTypes.LIKE:
            self.message = f'{self.from_user.username} liked your action with id {self.target_id}'
        elif self.type == NotificationTypes.COMMENT:
            self.message = f'{self.from_user.username} commented on your post with id {self.target_id}'
        elif self.type == NotificationTypes.POST:
            self.message = f'{self.from_user.username} created new post in channel with id {self.target_id}'

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)
