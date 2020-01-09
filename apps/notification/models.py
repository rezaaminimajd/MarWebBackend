from django.db import models


class NotificationTypes:
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMAND = 'command'
    DISLIKE = 'dislike'
    TYPES = (
        (FOLLOW, 'follow'),
        (LIKE, 'like'),
        (COMMAND, 'command'),
        (DISLIKE, 'dislike'),
    )


class Notification(models.Model):
    user_link = models.CharField(max_length=200)
    post_link = models.CharField(max_length=200, null=True, blank=True)
    notification_type = models.CharField(choices=NotificationTypes.TYPES, max_length=10)

