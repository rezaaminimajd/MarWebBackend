import os

from django.contrib.auth.models import User
from django.db import models

from polymorphic.models import PolymorphicModel


# Create your models here.

class UserActionTypes:
    POST = 'post'
    COMMENT = 'comment'
    TYPES = (
        (POST, 'post'),
        (COMMENT, 'comment')
    )


class LikeTypes:
    LIKE = 'like'
    DISLIKE = 'dislike'
    TYPES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    )


class UserActionTemplate(PolymorphicModel):
    user = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    body = models.TextField()
    type = models.CharField(max_length=20, choices=UserActionTypes.TYPES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def upload_path(self, filename):
        return os.path.join('private/', self.user.username, 'actions', self.type, str(self.id), filename)

    media = models.FileField(upload_to=upload_path, null=True, blank=True)

    @property
    def post_summary(self):
        return self.body[:len(self.body) // 4]

    def __str__(self):
        return f'id:{self.id}, username:{self.user.username}'


class Post(UserActionTemplate):
    title = models.CharField(max_length=200)
    channel = models.ForeignKey('channel.Channel', related_name='posts', on_delete=models.CASCADE)

    def pre_save(self):
        self.type = UserActionTypes.POST

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'id:{self.id}, username:{self.user.username}'


class Comment(UserActionTemplate):
    post_related = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    replies = models.ForeignKey('self', related_name='comments', on_delete=models.CASCADE, null=True, blank=True)

    def pre_save(self):
        self.type = UserActionTypes.COMMENT

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'id:{self.id}, username:{self.user.username}'


class Like(models.Model):
    target = models.ForeignKey('post.UserActionTemplate', related_name='likes', on_delete=models.CASCADE)
    liker = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=LikeTypes.TYPES, default=LikeTypes.LIKE)
